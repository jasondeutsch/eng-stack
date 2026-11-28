#!/usr/bin/env python3
"""Run local verification with owned POSIX server process groups and durable logs.
Lifecycle concept adapted from Anthropic webapp-testing (Apache-2.0).
This implementation replaces readiness, output handling, timeouts, and teardown.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
from urllib.parse import urlsplit
from urllib.request import build_opener, ProxyHandler, HTTPRedirectHandler
import uuid


def positive(value: str) -> float:
    number = float(value)
    if not 0 < number < float('inf'):
        raise argparse.ArgumentTypeError('must be finite and positive')
    return number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server', action='append', required=True, help='Shell command, repeated per server')
    parser.add_argument('--port', action='append', type=int, required=True, help='Unique localhost port per server')
    parser.add_argument('--ready-url', action='append', default=[], help='Optional localhost HTTP readiness URL per server')
    parser.add_argument('--cwd', type=Path, default=Path.cwd(), help='Workspace for servers and verification command')
    parser.add_argument('--log-dir', type=Path, required=True, help='Parent for a unique run directory; never removed')
    parser.add_argument('--startup-timeout', type=positive, default=60)
    parser.add_argument('--command-timeout', type=positive, default=600)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command[:1] == ['--']:
        args.command = args.command[1:]
    if os.name != 'posix':
        parser.error('requires POSIX process groups (macOS or Linux)')
    if not args.command or len(args.server) != len(args.port):
        parser.error('supply one --port per --server and a command after --')
    if len(set(args.port)) != len(args.port) or any(not 1 <= port <= 65535 for port in args.port):
        parser.error('ports must be unique integers from 1 to 65535')
    if args.ready_url and len(args.ready_url) != len(args.server):
        parser.error('supply a --ready-url per server, or omit all readiness URLs')
    for url, port in zip(args.ready_url, args.port):
        try:
            parsed = urlsplit(url)
            valid = parsed.scheme == 'http' and parsed.hostname in ('localhost', '127.0.0.1', '::1') and (parsed.port or 80) == port and not parsed.username and not parsed.password
        except ValueError:
            valid = False
        if not valid:
            parser.error('readiness URLs must be local HTTP URLs on the corresponding port, without credentials')
    args.cwd = args.cwd.resolve(strict=True)
    if not args.cwd.is_dir():
        parser.error('--cwd must be a directory')
    return args


def port_open(port: int) -> bool:
    for host in ('127.0.0.1', '::1'):
        try:
            with socket.create_connection((host, port), timeout=0.15):
                return True
        except OSError:
            pass
    return False


def group_alive(pid: int) -> bool:
    try:
        os.killpg(pid, 0)
        return True
    except ProcessLookupError:
        return False


def stop_owned(process: subprocess.Popen) -> None:
    # Each group was created by this run using start_new_session=True.
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        process.poll()  # Reap the group leader when it exits.
        if not group_alive(process.pid):
            break
        time.sleep(0.05)
    if group_alive(process.pid):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f'owned process {process.pid} did not exit after termination')


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, new_url):
        return None


def wait_ready(process: subprocess.Popen, port: int, url: str | None, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    opener = build_opener(ProxyHandler({}), NoRedirect())
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f'server on port {port} exited with {process.returncode}')
        ready = False
        if url:
            try:
                with opener.open(url, timeout=min(1, max(0.05, deadline-time.monotonic()))) as response:
                    ready = 200 <= response.status < 300 and urlsplit(response.url).hostname in ('localhost', '127.0.0.1', '::1')
            except (OSError, ValueError):
                pass
        else:
            ready = port_open(port)
        if ready:
            # Catch immediate startup failure rather than accepting an unrelated responder.
            time.sleep(0.1)
            if process.poll() is None:
                return
        time.sleep(0.1)
    raise TimeoutError(f'server readiness timed out on port {port}')


def interrupted(signum, frame):
    raise KeyboardInterrupt


def main() -> int:
    args = parse_args()
    owned = []
    logs = []
    run_dir = None
    outcome = {'workspace': str(args.cwd), 'status': 'error', 'exit_code': 2}
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        # Never attach to or shut down an existing instance.
        busy = [port for port in args.port if port_open(port)]
        if busy:
            raise RuntimeError(f'ports already in use: {busy}; choose isolated ports')
        args.log_dir.mkdir(parents=True, exist_ok=True)
        run_dir = args.log_dir.resolve() / ('run-' + uuid.uuid4().hex[:12])
        run_dir.mkdir()
        print(f'Evidence directory: {run_dir}', flush=True)
        outcome['servers'] = []
        for index, (command, port) in enumerate(zip(args.server, args.port)):
            log = (run_dir / f'server-{index+1}.log').open('wb')
            logs.append(log)
            process = subprocess.Popen(command, cwd=args.cwd, shell=True, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            owned.append(process)
            url = args.ready_url[index] if args.ready_url else None
            outcome['servers'].append({'pid': process.pid, 'port': port, 'readiness': 'http' if url else 'tcp-only', 'log': log.name})
            wait_ready(process, port, url, args.startup_timeout)
        log = (run_dir / 'verification.log').open('wb')
        logs.append(log)
        process = subprocess.Popen(args.command, cwd=args.cwd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        owned.append(process)
        try:
            code = process.wait(timeout=args.command_timeout)
        except subprocess.TimeoutExpired:
            raise TimeoutError('verification command timed out')
        # A check completing after its server crashed is not a verified run.
        dead = [p.pid for p in owned[:-1] if p.poll() is not None]
        if dead:
            raise RuntimeError(f'server exited during verification: {dead}')
        code = code if code >= 0 else 128 - code
        outcome.update(status='passed' if code == 0 else 'failed', exit_code=code)
    except KeyboardInterrupt:
        outcome.update(status='interrupted', exit_code=130)
    except (OSError, RuntimeError, TimeoutError) as error:
        outcome.update(error=str(error))
    finally:
        # Further terminal signals must not interrupt cleanup of our groups.
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        cleanup_errors = []
        for process in reversed(owned):
            try:
                stop_owned(process)
            except (OSError, RuntimeError) as error:
                cleanup_errors.append(str(error))
        for log in logs:
            log.close()
        if cleanup_errors:
            outcome.update(status='cleanup_failed', exit_code=2, cleanup_errors=cleanup_errors)
        if run_dir:
            (run_dir / 'result.json').write_text(json.dumps(outcome, indent=2)+'\n')
    print(json.dumps(outcome, indent=2), flush=True)
    return outcome['exit_code']


if __name__ == '__main__':
    sys.exit(main())
