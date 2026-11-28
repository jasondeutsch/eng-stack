#!/usr/bin/env python3
"""Create one attributed commit for a lifecycle hook invocation."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid


def git(*args):
    result = subprocess.run(["git", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def write_json(path, data):
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as output:
        json.dump(data, output)
        temporary = output.name
    os.replace(temporary, path)


def clean_line(value):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise RuntimeError("commit metadata must contain nonempty single-line strings")
    return value.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", help="project directory within the execution worktree")
    parser.add_argument("--type", default="chore")
    parser.add_argument("--scope")
    parser.add_argument("--description", required=True)
    parser.add_argument("--path", action="append", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9-]*", args.type):
        raise RuntimeError("invalid Conventional Commits type")
    if args.scope is not None and not re.fullmatch(r"[A-Za-z0-9_./-]+", args.scope):
        raise RuntimeError("invalid Conventional Commits scope")
    description = clean_line(args.description)
    context = json.load(sys.stdin)
    if context.get("version") != 1 or context.get("boundary") != "after":
        raise RuntimeError("committer requires version 1 after-hook context")
    if args.workspace:
        os.chdir(Path(args.workspace).resolve())
    execution = str(uuid.UUID(context["execution_id"]))
    invocation = str(uuid.UUID(context["invocation_id"]))
    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    workspace = Path.cwd().resolve()
    # Resolve user paths from the workspace, then anchor literal Git pathspecs
    # at the repository root so Git does not prefix the workspace a second time.
    paths = []
    for name in args.path:
        path = (workspace / name).resolve()
        if not path.is_relative_to(workspace):
            raise RuntimeError("commit paths must stay inside the workspace root")
        relative = str(path.relative_to(root))
        # Preserve existing root-workspace receipts for idempotent retries.
        prefix = ":(literal)" if workspace == root else ":(top,literal)"
        paths.append(prefix + relative)
    directory = Path(git("rev-parse", "--git-common-dir")).resolve() / "factory"
    receipts = directory / "commits"
    receipts.mkdir(parents=True, exist_ok=True)
    with (directory / "hooks.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        branch_receipt = directory / "executions" / (execution + ".json")
        if not branch_receipt.exists():
            raise RuntimeError("execution has no prepared branch receipt")
        owner = json.loads(branch_receipt.read_text())
        if owner.get("mode") != "worktree" or owner.get("state") != "prepared" or Path(owner["workspace"]).resolve() != root:
            raise RuntimeError("checkout is not this execution's prepared worktree")
        branch = owner["branch"]
        if git("branch", "--show-current") != branch:
            raise RuntimeError("checkout is not on the execution branch")
        subject = args.type + ("(" + args.scope + ")" if args.scope else "") + ": " + description
        trailers = ["Execution-ID: " + execution, "Hook-Invocation: " + invocation]
        if context.get("stage"):
            trailers.append("Stage: " + clean_line(context["stage"]))
        if context.get("step"):
            trailers.append("Step: " + clean_line(context["step"]))
        for person in context.get("participants", []):
            identity = "/".join(clean_line(person[key]) for key in ("agent", "instance_id", "step"))
            visit, attempt = int(person["visit"]), int(person["attempt"])
            if visit < 1 or attempt < 1:
                raise RuntimeError("participant visit and attempt must be positive")
            trailers.append(f"Agent-Invocation: {identity}/v{visit}/t{attempt} outcome={clean_line(person['outcome'])}")
        message = subject + "\n\n" + "\n".join(trailers) + "\n"
        receipt = receipts / (invocation + ".json")
        request = {"message": message, "paths": paths}
        prior = json.loads(receipt.read_text()) if receipt.exists() else None
        if prior and prior["request"] != request:
            raise RuntimeError("hook invocation was already used with different commit arguments or context")
        # Recover a commit made just before process/DB interruption. Search only
        # the current branch ancestry, then check the exact trailer line.
        candidates = git("log", "--format=%H", "--fixed-strings", "--grep=Hook-Invocation: " + invocation).splitlines()
        for candidate in candidates:
            committed = git("show", "-s", "--format=%B", candidate)
            if "Hook-Invocation: " + invocation in committed.splitlines():
                if committed != message.strip():
                    raise RuntimeError("an existing invocation commit has a different message; inspect repository hooks")
                result = {"state": "committed", "commit": candidate, "request": request}
                write_json(receipt, result)
                print(json.dumps(result))
                return
        if prior and prior["state"] == "no_changes":
            print(json.dumps(prior))
            return
        if prior and prior["state"] == "committed":
            raise RuntimeError("recorded commit is no longer in branch history")
        if git("ls-files", "--unmerged"):
            raise RuntimeError("checkout contains unresolved conflicts")
        parent = git("rev-parse", "HEAD")
        if prior and prior["state"] == "staged" and prior["parent"] != parent:
            raise RuntimeError("HEAD changed since this hook staged its work; inspect the unrecognized commit before retrying")
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode
        if staged not in (0, 1):
            raise RuntimeError("could not inspect staged changes")
        if staged:
            if not prior or prior["state"] != "staged" or prior["parent"] != parent or prior["tree"] != git("write-tree"):
                raise RuntimeError("index contains changes not owned by this hook; inspect staged files")
        git("add", "--all", "--", *paths)
        tree = git("write-tree")
        if tree == git("rev-parse", "HEAD^{tree}"):
            result = {"state": "no_changes", "request": request}
            write_json(receipt, result)
            print(json.dumps(result))
            return
        write_json(receipt, {"state": "staged", "request": request, "tree": tree, "parent": parent})
        with tempfile.NamedTemporaryFile(mode="w", dir=directory, delete=False) as output:
            output.write(message)
            message_path = output.name
        try:
            # Normal identity, hooks and signing apply. Never use --no-verify.
            git("commit", "--file", message_path)
        finally:
            Path(message_path).unlink(missing_ok=True)
        commit = git("rev-parse", "HEAD")
        if git("show", "-s", "--format=%B", commit) != message.strip():
            raise RuntimeError("repository hook changed the generated commit message; inspect the created commit")
        result = {"state": "committed", "commit": commit, "request": request}
        write_json(receipt, result)
        print(json.dumps(result))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, KeyError, TypeError, OSError) as error:
        print("committer: " + str(error), file=sys.stderr)
        sys.exit(1)
