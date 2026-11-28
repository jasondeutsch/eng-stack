#!/usr/bin/env python3
# Adapted from OpenAI gh-fix-ci, Apache-2.0; see ../SOURCES.md and ../LICENSE.
# Local changes: explicit check states, structured incomplete/error outcomes,
# bounded subprocess calls, valid nonzero gh JSON handling, and PR-head evidence.
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from urllib.parse import urlsplit
from pathlib import Path
from shutil import which
from typing import Any, Sequence

FAILURE_CONCLUSIONS = {
    "failure",
    "cancelled",
    "timed_out",
    "action_required",
}

FAILURE_STATES = {
    "failure",
    "error",
    "cancelled",
    "timed_out",
    "action_required",
}

FAILURE_BUCKETS = {"fail"}

FAILURE_MARKERS = (
    "error",
    "fail",
    "failed",
    "traceback",
    "exception",
    "assert",
    "panic",
    "fatal",
    "timeout",
    "segmentation fault",
)

DEFAULT_MAX_LINES = 160
DEFAULT_CONTEXT_LINES = 30
PENDING_LOG_MARKERS = (
    "still in progress",
    "log will be available when it is complete",
)


class GhResult:
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def run_gh_command(args: Sequence[str], cwd: Path) -> GhResult:
    process = subprocess.run(
        ["gh", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=60,
    )
    return GhResult(process.returncode, process.stdout, process.stderr)


def run_gh_command_raw(args: Sequence[str], cwd: Path) -> tuple[int, bytes, str]:
    process = subprocess.run(
        ["gh", *args],
        cwd=cwd,
        capture_output=True,
        timeout=60,
    )
    stderr = process.stderr.decode(errors="replace")
    return process.returncode, process.stdout, stderr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect failing GitHub PR checks, fetch GitHub Actions logs, and extract a "
            "failure snippet."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--repo", default=".", help="Path inside the target Git repository.")
    parser.add_argument(
        "--pr", default=None, help="PR number or URL (defaults to current branch PR)."
    )
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    parser.add_argument("--context", type=int, default=DEFAULT_CONTEXT_LINES)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text output.")
    return parser.parse_args()


def check_status(check: dict[str, Any]) -> str:
    if is_failing(check):
        return "failed"
    values = {normalize_field(check.get(field)) for field in ("state", "status", "conclusion", "bucket")}
    if values & {"pending", "queued", "in_progress", "waiting", "requested", "expected"}:
        return "pending"
    if values & {"skipped", "neutral", "cancel", "cancelled"}:
        return "skipped"
    if values & {"success", "pass"}:
        return "successful"
    return "unavailable"


def pr_snapshot(pr_value: str, root: Path) -> dict[str, Any] | None:
    result = run_gh_command(["pr", "view", pr_value, "--json", "number,url,headRefOid"], cwd=root)
    if result.returncode:
        return None
    try:
        data = json.loads(result.stdout)
        return data if isinstance(data, dict) and data.get("headRefOid") and data.get("url") else None
    except json.JSONDecodeError:
        return None


def diagnose(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    root = find_git_root(Path(args.repo))
    if root is None:
        return {"status": "unavailable", "error": "Not inside a Git repository"}, 2
    if not ensure_gh_available(root):
        return {"status": "unavailable", "error": "GitHub CLI or authentication unavailable"}, 2
    pr_value = resolve_pr(args.pr, root)
    if pr_value is None:
        return {"status": "unavailable", "error": "Could not resolve PR"}, 2
    snapshot = pr_snapshot(pr_value, root)
    if snapshot is None:
        return {"status": "unavailable", "error": "Could not establish PR head"}, 2
    repo_slug = fetch_repo_slug(root)
    parsed = urlsplit(snapshot["url"])
    # run/job commands below execute in this repo; reject cross-repository PR input.
    if parsed.path.strip("/").split("/pull/")[0].lower() != (repo_slug or "").lower():
        return {"status": "unavailable", "error": "PR is not in --repo; select its checkout"}, 2
    checks = fetch_checks(pr_value, root)
    if checks is None:
        return {"status": "unavailable", "pr": snapshot, "error": "Could not retrieve checks"}, 2
    results = []
    for check in checks:
        state = check_status(check)
        url = check.get("detailsUrl") or check.get("link") or ""
        row = {"name": check.get("name", ""), "state": state, "url": url}
        if state == "failed":
            parts = urlsplit(url)
            is_local_action = parts.netloc == parsed.netloc and parts.path.startswith("/" + repo_slug + "/actions/runs/")
            if is_local_action:
                row["diagnostic"] = analyze_check(check, root, max(1,args.max_lines), max(1,args.context))
                run = row["diagnostic"].get("run") or {}
                if run.get("headSha") and run["headSha"] != snapshot["headRefOid"]:
                    row["diagnostic"]["sourceMismatch"] = "Run SHA differs from PR head; it may be a merge revision. Verify provenance before applying a repair."
            else:
                row["diagnostic"] = {"status": "external", "note": "External check; report URL only"}
        results.append(row)
    states = {row["state"] for row in results}
    if "failed" in states:
        status, code = "failed", 1
    elif results and states == {"successful"}:
        status, code = "successful", 0
    else:
        status, code = "incomplete", 2
    return {"status":status, "pr":snapshot, "checks":results,
            "scope":"All checks reported by gh, not proof that every required check exists or acceptance is met"}, code


def main() -> int:
    args = parse_args()
    try:
        data, code = diagnose(args)
    except (OSError, subprocess.TimeoutExpired, ValueError) as error:
        data, code = {"status":"unavailable", "error": str(error)}, 2
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("CI status:", data["status"])
        if data.get("error"):
            print(data["error"])
        if data.get("pr"):
            print(data["pr"]["url"], "head:", data["pr"]["headRefOid"])
        for row in data.get("checks", []):
            print(f"{row['state']}: {row['name']} {row['url']}")
            diagnostic = row.get("diagnostic", {})
            for field in ("note", "error", "sourceMismatch", "logSnippet"):
                if diagnostic.get(field):
                    print(diagnostic[field])
    return code


def find_git_root(start: Path) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        capture_output=True,
        timeout=60,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def ensure_gh_available(repo_root: Path) -> bool:
    if which("gh") is None:
        print("Error: gh is not installed or not on PATH.", file=sys.stderr)
        return False
    result = run_gh_command(["auth", "status"], cwd=repo_root)
    if result.returncode == 0:
        return True
    message = (result.stderr or result.stdout or "").strip()
    print(message or "Error: gh not authenticated.", file=sys.stderr)
    return False


def resolve_pr(pr_value: str | None, repo_root: Path) -> str | None:
    if pr_value:
        return pr_value
    result = run_gh_command(["pr", "view", "--json", "number"], cwd=repo_root)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        print(message or "Error: unable to resolve PR.", file=sys.stderr)
        return None
    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        print("Error: unable to parse PR JSON.", file=sys.stderr)
        return None
    number = data.get("number")
    if not number:
        print("Error: no PR number found.", file=sys.stderr)
        return None
    return str(number)


def fetch_checks(pr_value: str, repo_root: Path) -> list[dict[str, Any]] | None:
    primary_fields = ["name", "state", "bucket", "link", "startedAt", "completedAt", "workflow"]
    result = run_gh_command(
        ["pr", "checks", pr_value, "--json", ",".join(primary_fields)],
        cwd=repo_root,
    )
    try:
        parsed = json.loads(result.stdout)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    if result.returncode != 0:
        message = "\n".join(filter(None, [result.stderr, result.stdout])).strip()
        available_fields = parse_available_fields(message)
        if available_fields:
            fallback_fields = [
                "name",
                "state",
                "bucket",
                "link",
                "startedAt",
                "completedAt",
                "workflow",
            ]
            selected_fields = [field for field in fallback_fields if field in available_fields]
            if not selected_fields:
                print("Error: no usable fields available for gh pr checks.", file=sys.stderr)
                return None
            result = run_gh_command(
                ["pr", "checks", pr_value, "--json", ",".join(selected_fields)],
                cwd=repo_root,
            )
            try:
                parsed = json.loads(result.stdout)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
            if result.returncode != 0:
                message = (result.stderr or result.stdout or "").strip()
                print(message or "Error: gh pr checks failed.", file=sys.stderr)
                return None
        else:
            print(message or "Error: gh pr checks failed.", file=sys.stderr)
            return None
    try:
        data = json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        print("Error: unable to parse checks JSON.", file=sys.stderr)
        return None
    if not isinstance(data, list):
        print("Error: unexpected checks JSON shape.", file=sys.stderr)
        return None
    return data


def is_failing(check: dict[str, Any]) -> bool:
    conclusion = normalize_field(check.get("conclusion"))
    if conclusion in FAILURE_CONCLUSIONS:
        return True
    state = normalize_field(check.get("state") or check.get("status"))
    if state in FAILURE_STATES:
        return True
    bucket = normalize_field(check.get("bucket"))
    return bucket in FAILURE_BUCKETS


def analyze_check(
    check: dict[str, Any],
    repo_root: Path,
    max_lines: int,
    context: int,
) -> dict[str, Any]:
    url = check.get("detailsUrl") or check.get("link") or ""
    run_id = extract_run_id(url)
    job_id = extract_job_id(url)
    base: dict[str, Any] = {
        "name": check.get("name", ""),
        "detailsUrl": url,
        "runId": run_id,
        "jobId": job_id,
    }

    if run_id is None:
        base["status"] = "external"
        base["note"] = "No GitHub Actions run id detected in detailsUrl."
        return base

    metadata = fetch_run_metadata(run_id, repo_root)
    log_text, log_error, log_status = fetch_check_log(
        run_id=run_id,
        job_id=job_id,
        repo_root=repo_root,
    )

    if log_status == "pending":
        base["status"] = "log_pending"
        base["note"] = log_error or "Logs are not available yet."
        if metadata:
            base["run"] = metadata
        return base

    if log_error:
        base["status"] = "log_unavailable"
        base["error"] = log_error
        if metadata:
            base["run"] = metadata
        return base

    snippet = extract_failure_snippet(log_text, max_lines=max_lines, context=context)
    base["status"] = "ok"
    base["run"] = metadata or {}
    base["logSnippet"] = snippet
    base["logTail"] = tail_lines(log_text, max_lines)
    return base


def extract_run_id(url: str) -> str | None:
    if not url:
        return None
    for pattern in (r"/actions/runs/(\d+)",):
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_job_id(url: str) -> str | None:
    if not url:
        return None
    match = re.search(r"/actions/runs/\d+/job/(\d+)", url)
    if match:
        return match.group(1)
    match = re.search(r"/job/(\d+)", url)
    if match:
        return match.group(1)
    return None


def fetch_run_metadata(run_id: str, repo_root: Path) -> dict[str, Any] | None:
    fields = [
        "conclusion",
        "status",
        "workflowName",
        "name",
        "event",
        "headBranch",
        "headSha",
        "url",
    ]
    result = run_gh_command(["run", "view", run_id, "--json", ",".join(fields)], cwd=repo_root)
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def fetch_check_log(
    run_id: str,
    job_id: str | None,
    repo_root: Path,
) -> tuple[str, str, str]:
    log_text, log_error = fetch_run_log(run_id, repo_root)
    if not log_error:
        return log_text, "", "ok"

    if is_log_pending_message(log_error) and job_id:
        job_log, job_error = fetch_job_log(job_id, repo_root)
        if job_log:
            return job_log, "", "ok"
        if job_error and is_log_pending_message(job_error):
            return "", job_error, "pending"
        if job_error:
            return "", job_error, "error"
        return "", log_error, "pending"

    if is_log_pending_message(log_error):
        return "", log_error, "pending"

    return "", log_error, "error"


def fetch_run_log(run_id: str, repo_root: Path) -> tuple[str, str]:
    result = run_gh_command(["run", "view", run_id, "--log"], cwd=repo_root)
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "").strip()
        return "", error or "gh run view failed"
    return result.stdout, ""


def fetch_job_log(job_id: str, repo_root: Path) -> tuple[str, str]:
    repo_slug = fetch_repo_slug(repo_root)
    if not repo_slug:
        return "", "Error: unable to resolve repository name for job logs."
    endpoint = f"/repos/{repo_slug}/actions/jobs/{job_id}/logs"
    returncode, stdout_bytes, stderr = run_gh_command_raw(["api", endpoint], cwd=repo_root)
    if returncode != 0:
        message = (stderr or stdout_bytes.decode(errors="replace")).strip()
        return "", message or "gh api job logs failed"
    if is_zip_payload(stdout_bytes):
        return "", "Job logs returned a zip archive; unable to parse."
    return stdout_bytes.decode(errors="replace"), ""


def fetch_repo_slug(repo_root: Path) -> str | None:
    result = run_gh_command(["repo", "view", "--json", "nameWithOwner"], cwd=repo_root)
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return None
    name_with_owner = data.get("nameWithOwner")
    if not name_with_owner:
        return None
    return str(name_with_owner)


def normalize_field(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def parse_available_fields(message: str) -> list[str]:
    if "Available fields:" not in message:
        return []
    fields: list[str] = []
    collecting = False
    for line in message.splitlines():
        if "Available fields:" in line:
            collecting = True
            continue
        if not collecting:
            continue
        field = line.strip()
        if not field:
            continue
        fields.append(field)
    return fields


def is_log_pending_message(message: str) -> bool:
    lowered = message.lower()
    return any(marker in lowered for marker in PENDING_LOG_MARKERS)


def is_zip_payload(payload: bytes) -> bool:
    return payload.startswith(b"PK")


def extract_failure_snippet(log_text: str, max_lines: int, context: int) -> str:
    lines = log_text.splitlines()
    if not lines:
        return ""

    marker_index = find_failure_index(lines)
    if marker_index is None:
        return "\n".join(lines[-max_lines:])

    start = max(0, marker_index - context)
    end = min(len(lines), marker_index + context)
    window = lines[start:end]
    if len(window) > max_lines:
        window = window[-max_lines:]
    return "\n".join(window)


def find_failure_index(lines: Sequence[str]) -> int | None:
    for idx in range(len(lines) - 1, -1, -1):
        lowered = lines[idx].lower()
        if any(marker in lowered for marker in FAILURE_MARKERS):
            return idx
    return None


def tail_lines(text: str, max_lines: int) -> str:
    if max_lines <= 0:
        return ""
    lines = text.splitlines()
    return "\n".join(lines[-max_lines:])


if __name__ == "__main__":
    raise SystemExit(main())

