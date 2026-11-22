#!/usr/bin/env python3
"""Prepare or release one retained Git worktree per execution. Reads hook JSON on stdin."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid


def git(repository, *args):
    result = subprocess.run(['git', '-C', str(repository), *args], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'git command failed')
    return result.stdout.strip()


def write_json(path, value):
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as output:
        json.dump(value, output)
        temporary = output.name
    os.replace(temporary, path)


def branch_exists(repository, branch):
    result = subprocess.run(['git', '-C', str(repository), 'show-ref', '--verify', '--quiet', 'refs/heads/' + branch])
    if result.returncode not in (0, 1):
        raise RuntimeError('could not inspect execution branch')
    return result.returncode == 0


def verify_worktree(workspace, repository, branch):
    if Path(git(workspace, 'rev-parse', '--show-toplevel')).resolve() != workspace:
        raise RuntimeError('workspace is not its own worktree root')
    common = Path(git(workspace, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve()
    if common != repository:
        raise RuntimeError('workspace belongs to another repository')
    if git(workspace, 'branch', '--show-current') != branch:
        raise RuntimeError('workspace is no longer on its recorded execution branch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', required=True, help='source repository or a directory inside it')
    parser.add_argument('--workspace', required=True, help='execution worktree location, relative to hook cwd or absolute')
    parser.add_argument('--base', default='HEAD')
    parser.add_argument('--prefix', default='execution/')
    parser.add_argument('--release', action='store_true', help='mark successful completion; retain worktree and branch')
    args = parser.parse_args()
    context = json.load(sys.stdin)
    boundary = 'after' if args.release else 'before'
    if context.get('version') != 1 or context.get('scope') != 'execution' or context.get('boundary') != boundary:
        raise RuntimeError('worktree utility requires matching version 1 execution before/after context')
    execution = str(uuid.UUID(context['execution_id']))
    invocation = str(uuid.UUID(context['invocation_id']))
    source = Path(args.repository).resolve()
    workspace = Path(args.workspace).resolve()
    repository = Path(git(source, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve()
    source_root = Path(git(source, 'rev-parse', '--show-toplevel')).resolve()
    if workspace == source_root or workspace.is_relative_to(repository):
        raise RuntimeError('workspace must be a separate checkout outside Git metadata')
    branch = args.prefix + execution
    git(source, 'check-ref-format', '--branch', branch)
    directory = repository / 'factory'
    receipts = directory / 'executions'
    receipts.mkdir(parents=True, exist_ok=True)
    receipt = receipts / (execution + '.json')
    with (directory / 'hooks.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        prior = json.loads(receipt.read_text()) if receipt.exists() else None
        request = {'mode': 'worktree', 'source': str(source_root), 'workspace': str(workspace),
                   'branch': branch, 'base': args.base}
        if prior and any(prior.get(key) != value for key, value in request.items()):
            raise RuntimeError('execution receipt differs from this worktree configuration')
        if args.release:
            if not prior or prior['state'] not in ('prepared', 'released'):
                raise RuntimeError('execution has no prepared worktree to release')
            verify_worktree(workspace, repository, branch)
            if prior.get('release_invocation') not in (None, invocation):
                raise RuntimeError('worktree was released by a different hook invocation')
            prior.update(state='released', release_invocation=invocation)
            write_json(receipt, prior)
            print(json.dumps(prior))
            return
        if prior:
            if prior['invocation_id'] != invocation:
                raise RuntimeError('worktree was prepared by a different hook invocation')
            if workspace.exists():
                verify_worktree(workspace, repository, branch)
                if prior['state'] == 'preparing' and git(workspace, 'rev-parse', 'HEAD') != prior['starting_commit']:
                    raise RuntimeError('interrupted worktree preparation has unexpected commits')
                if prior['state'] != 'released':
                    prior['state'] = 'prepared'
                write_json(receipt, prior)
                print(json.dumps(prior))
                return
            if prior['state'] != 'preparing':
                raise RuntimeError('recorded worktree is missing; inspect it rather than silently recreating it')
        else:
            if workspace.exists():
                raise RuntimeError('workspace already exists without this execution receipt')
            if branch_exists(source, branch):
                raise RuntimeError('execution branch already exists without this execution receipt')
            prior = dict(request, version=1, execution_id=execution, invocation_id=invocation,
                         starting_commit=git(source, 'rev-parse', '--verify', args.base + '^{commit}'), state='preparing')
            write_json(receipt, prior)
        # A receipt predates Git effects, allowing a retry to verify interrupted
        # preparation without resetting or adopting an unrelated checkout.
        workspace.parent.mkdir(parents=True, exist_ok=True)
        if branch_exists(source, branch):
            if git(source, 'rev-parse', 'refs/heads/' + branch) != prior['starting_commit']:
                raise RuntimeError('interrupted preparation branch has unexpected commits')
            git(source, 'worktree', 'add', str(workspace), branch)
        else:
            git(source, 'worktree', 'add', '-b', branch, str(workspace), prior['starting_commit'])
        verify_worktree(workspace, repository, branch)
        prior['state'] = 'prepared'
        write_json(receipt, prior)
        print(json.dumps(prior))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, KeyError, OSError) as error:
        print('worktree: ' + str(error), file=sys.stderr)
        sys.exit(1)
