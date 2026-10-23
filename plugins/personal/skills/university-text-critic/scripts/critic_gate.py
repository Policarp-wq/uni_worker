#!/usr/bin/env python3
"""Local review ledger and hash-bound DOCX gate; Python 3.10+, Linux/WSL or macOS."""

import argparse
import difflib
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import uuid

if sys.platform == "win32":
    print("BLOCKED: Native Windows is unsupported: fcntl is unavailable. "
          "You must replace fcntl.flock() with Windows-compatible file locking "
          "that preserves protection against concurrent writes. Critic review and DOCX approval remain unavailable until then.",
          file=sys.stderr)
    raise SystemExit(2)

import fcntl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prose_gate  # noqa: E402


POLISH_LIMIT = 2
POLISH_LINES = 20


class GateError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"Expected a JSON object: {path}")
    return data


def atomic_json(path, data):
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def text_file(path, suffixes=(".md", ".txt", ".rst")):
    require(path.suffix.lower() in suffixes, f"Readable text requiring no conversion is needed: {path}")
    content = path.read_text(encoding="utf-8")
    require(content.strip() and "\ufffd" not in content and "\x00" not in content,
            f"Empty or corrupt text: {path}")
    return content


def snapshot(source, context):
    text_file(source, (".md",))
    require(context.parent == source.parent, "Context must be in the work folder")
    data = read_json(context)
    for key in ("subject", "topic"):
        require(isinstance(data.get(key), str) and data[key].strip(), f"Missing value for field {key}")
    requirements = data.get("requirements")
    require(isinstance(requirements, list) and requirements and
            all(isinstance(item, str) and item.strip() for item in requirements),
            "A nonempty requirements list from the assignment is required")
    previous = data.get("previous")
    require(type(data.get("previous_exists")) is bool and isinstance(previous, list),
            "Provide previous_exists (true/false) and a previous list")
    require(data["previous_exists"] == bool(previous), "previous_exists contradicts previous")
    assignment = data.get("assignment_files", [])
    require(isinstance(assignment, list), "assignment_files must be a list")
    files = {str(source): digest(source), str(context): digest(context)}
    for name in previous + assignment:
        require(isinstance(name, str) and name.strip(), "A source material path is required")
        path = (context.parent / name).resolve(strict=True)
        require(path != source, "The current work cannot be its own source material")
        text_file(path)
        files[str(path)] = digest(path)
    return files


@contextmanager
def ledger(source, create=False):
    source = Path(source).resolve(strict=True)
    state_path = source.parent / ".critic-state.json"
    lock_path = source.parent / ".critic-lock"
    require(create or lock_path.is_file(), "No critic review; DOCX is blocked")
    with lock_path.open("a+" if create else "r") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if state_path.exists():
            state = read_json(state_path)
            require(state.get("version") == 1 and state.get("source") == str(source),
                    "State belongs to another source; human intervention is required")
            attempts = state.get("attempts")
            current_cycle = state.get("current_cycle", 1)
            resolutions = state.get("human_resolutions", [])
            require(isinstance(attempts, list) and type(current_cycle) is int and
                    current_cycle >= 1 and isinstance(resolutions, list) and
                    current_cycle == len(resolutions) + 1,
                    "Corrupt cycle history; human intervention is required")
            counts = {}
            previous_cycle = 1
            for item in attempts:
                require(isinstance(item, dict), "Corrupt attempt history; human intervention is required")
                cycle = item.get("cycle", 1)
                require(type(cycle) is int and 1 <= cycle <= current_cycle and
                        cycle >= previous_cycle,
                        "Corrupt cycle history; human intervention is required")
                counts[cycle] = counts.get(cycle, 0) + 1
                require(counts[cycle] <= 3 and item.get("attempt") == counts[cycle],
                        "Corrupt attempt history; human intervention is required")
                previous_cycle = cycle
            require(all(isinstance(item, dict) and item.get("from_cycle") == i and
                        item.get("to_cycle") == i + 1 and isinstance(item.get("decision"), str) and
                        item["decision"].strip()
                        for i, item in enumerate(resolutions, 1)),
                    "Corrupt author resolution record; human intervention is required")
        else:
            require(create, "No review history; DOCX is blocked")
            require(not (source.parent / ".critic-approve").exists() and
                    not (source.parent / ".critic").exists(),
                    "Review artifacts exist without history; human intervention is required")
            state = {"version": 1, "source": str(source), "attempts": [],
                     "current_cycle": 1, "human_resolutions": []}
        yield source, state_path, state


def begin(source, context):
    context = Path(context).resolve(strict=True)
    try:
        prose_gate.require_compression(source)
    except prose_gate.GateError as error:
        raise GateError(str(error)) from error
    with ledger(source, create=True) as (source, state_path, state):
        files = snapshot(source, context)
        attempts = state["attempts"]
        cycle = state.get("current_cycle", 1)
        cycle_attempts = [item for item in attempts if item.get("cycle", 1) == cycle]
        require(len(cycle_attempts) < 3,
                "HUMAN_REQUIRED: 3/3 attempts used in the current cycle; present reasons and reviews to the human")
        require(not attempts or attempts[-1].get("verdict") != "pending",
                "The previous critic is still running; wait or stop it and run cancel")
        require(all(item.get("verdict") != "pending" for item in state.get("polishes", [])),
                "A polish review is still running; wait or stop it and run polish-cancel")
        number = len(cycle_attempts) + 1
        report_dir = source.parent / ".critic"
        report_dir.mkdir(exist_ok=True)
        report_name = f"review-{number}.md" if cycle == 1 else f"cycle-{cycle}-review-{number}.md"
        record = {"cycle": cycle, "attempt": number, "ticket": uuid.uuid4().hex,
                  "report": str(report_dir / report_name),
                  "source": str(source), "context": str(context),
                  "snapshot": files, "verdict": "pending", "started": timestamp()}
        attempts.append(record)
        atomic_json(state_path, state)
        return record


def pending(state, ticket):
    require(state["attempts"], "No review has been started")
    record = state["attempts"][-1]
    require(record.get("ticket") == ticket and record.get("verdict") == "pending",
            "Invalid ticket or attempt already finished")
    return record


def finish(source, ticket, reviewer, verdict):
    require(verdict in ("approve", "revise", "context_error"), "Unknown verdict")
    require(isinstance(reviewer, str) and reviewer.strip(), "An independent critic ID or invocation label is required")
    with ledger(source) as (source, state_path, state):
        record = pending(state, ticket)
        require(snapshot(source, Path(record["context"])) == record["snapshot"],
                "Inputs changed after begin; approval is blocked, cancel and start another attempt")
        report = Path(record["report"])
        content = text_file(report, (".md",))
        require(f"Вердикт: {verdict.upper()}" in content,
                "The review verdict does not match finish")
        record.update(verdict=verdict, reviewer=reviewer, finished=timestamp(),
                      report_sha256=digest(report))
        if verdict == "approve":
            keep_copy(source, record, f"approved-c{record.get('cycle', 1)}-a{record['attempt']}.md")
        atomic_json(state_path, state)
        if verdict == "approve":
            atomic_json(source.parent / ".critic-approve", record)
        return {"verdict": verdict, "cycle": record.get("cycle", 1),
                "attempt": record["attempt"], "report": str(report)}


def keep_copy(source, record, name):
    copy = Path(record["report"]).parent / name
    copy.write_bytes(source.read_bytes())
    record["approved_copy"] = str(copy)


def current_approval(state):
    """The approved attempt of the current cycle, its polish records and the record now in force."""
    cycle = state.get("current_cycle", 1)
    attempts = [item for item in state["attempts"] if item.get("cycle", 1) == cycle]
    require(attempts, "No completed review in the current cycle")
    last = attempts[-1]
    require(last.get("verdict") == "approve", "The latest attempt in the current cycle is not approved")
    polishes = [item for item in state.get("polishes", [])
                if item.get("cycle") == cycle and item.get("attempt") == last["attempt"]]
    approved = [item for item in polishes if item.get("verdict") == "approve"]
    return last, polishes, approved[-1] if approved else last


def polish_begin(source):
    with ledger(source) as (source, state_path, state):
        last, polishes, approval = current_approval(state)
        require(all(item.get("verdict") != "pending" for item in polishes),
                "A polish review is still running; wait or stop it and run polish-cancel")
        require(len(polishes) < POLISH_LIMIT,
                f"{POLISH_LIMIT} polish reviews used for this approval; use a regular attempt")
        base = Path(approval.get("approved_copy", ""))
        require(approval.get("approved_copy") and base.is_file() and
                digest(base) == approval["snapshot"][str(source)],
                "The approved text is not stored; polish is unavailable, use a regular attempt")
        files = snapshot(source, Path(last["context"]))
        require(files[str(source)] != approval["snapshot"][str(source)],
                "The text is unchanged; the approval is still valid")
        others = {key: value for key, value in files.items() if key != str(source)}
        require(others == {key: value for key, value in approval["snapshot"].items() if key != str(source)},
                "Context or materials changed; a regular attempt is required")
        try:
            prose_gate.require_compression(source)
        except prose_gate.GateError as error:
            raise GateError(str(error)) from error
        diff = list(difflib.unified_diff(
            base.read_text(encoding="utf-8").splitlines(keepends=True),
            source.read_text(encoding="utf-8").splitlines(keepends=True),
            "approved", "current", n=2))
        changed = sum(1 for line in diff if line[:1] in "+-" and not line.startswith(("+++", "---")))
        require(changed <= POLISH_LINES,
                f"The edit changes {changed} lines, more than {POLISH_LINES}; use a regular attempt")
        number = len(polishes) + 1
        report_dir = source.parent / ".critic"
        name = f"polish-c{last.get('cycle', 1)}-a{last['attempt']}-{number}"
        diff_path = report_dir / f"{name}.diff"
        diff_path.write_text("".join(diff), encoding="utf-8")
        record = {"kind": "polish", "cycle": last.get("cycle", 1), "attempt": last["attempt"],
                  "polish": number, "ticket": uuid.uuid4().hex,
                  "report": str(report_dir / f"{name}.md"), "diff": str(diff_path),
                  "approved_review": approval["report"], "source": str(source),
                  "context": last["context"], "snapshot": files, "verdict": "pending",
                  "started": timestamp()}
        state.setdefault("polishes", []).append(record)
        atomic_json(state_path, state)
        return record


def pending_polish(state, ticket):
    polishes = state.get("polishes", [])
    require(polishes, "No polish review has been started")
    record = polishes[-1]
    require(record.get("ticket") == ticket and record.get("verdict") == "pending",
            "Invalid ticket or polish review already finished")
    return record


def polish_finish(source, ticket, reviewer, verdict):
    require(verdict in ("approve", "revise"), "Unknown verdict")
    require(isinstance(reviewer, str) and reviewer.strip(), "An independent critic ID or invocation label is required")
    with ledger(source) as (source, state_path, state):
        record = pending_polish(state, ticket)
        require(snapshot(source, Path(record["context"])) == record["snapshot"],
                "Inputs changed after polish-begin; cancel and start again")
        report = Path(record["report"])
        content = text_file(report, (".md",))
        require(f"Вердикт: {verdict.upper()}" in content, "The review verdict does not match finish")
        record.update(verdict=verdict, reviewer=reviewer, finished=timestamp(),
                      report_sha256=digest(report))
        if verdict == "approve":
            keep_copy(source, record, Path(record["report"]).stem + "-approved.md")
        atomic_json(state_path, state)
        if verdict == "approve":
            atomic_json(source.parent / ".critic-approve", record)
        return {"verdict": verdict, "cycle": record["cycle"], "attempt": record["attempt"],
                "polish": record["polish"], "report": str(report)}


def polish_cancel(source, ticket, reason):
    require(isinstance(reason, str) and reason.strip(), "Provide the cancellation reason")
    with ledger(source) as (_, state_path, state):
        record = pending_polish(state, ticket)
        record.update(verdict="cancelled", reason=reason, finished=timestamp())
        atomic_json(state_path, state)
        return {"verdict": "cancelled", "polish": record["polish"]}


def cancel(source, ticket, reason):
    require(isinstance(reason, str) and reason.strip(), "Provide the cancellation reason")
    with ledger(source) as (_, state_path, state):
        record = pending(state, ticket)
        record.update(verdict="cancelled", reason=reason, finished=timestamp())
        atomic_json(state_path, state)
        return {"verdict": "cancelled", "attempt": record["attempt"],
                "cycle": record.get("cycle", 1)}


def approval_is_stale(source, attempt):
    """True when inputs changed after an approved attempt, so its approval no longer holds."""
    try:
        return snapshot(source, Path(attempt["context"])) != attempt["snapshot"]
    except (OSError, ValueError, KeyError, TypeError, GateError):
        return True


def resolve(source, decision, resolved_by="author"):
    require(isinstance(decision, str) and decision.strip(), "Provide the author decision")
    require(isinstance(resolved_by, str) and resolved_by.strip(), "Identify who resolved the dispute")
    with ledger(source) as (resolved_source, state_path, state):
        cycle = state.get("current_cycle", 1)
        attempts = [item for item in state["attempts"] if item.get("cycle", 1) == cycle]
        require(len(attempts) == 3 and all(item.get("verdict") != "pending" for item in attempts),
                "HUMAN_REQUIRED: A new cycle requires three completed attempts")
        last = attempts[-1]
        disputed = last.get("verdict") in ("revise", "context_error")
        stale = last.get("verdict") == "approve" and approval_is_stale(resolved_source, last)
        require(disputed or stale,
                "The last attempt has no unresolved dispute and its approval is still valid; an approved cycle cannot be reset")
        resolution = {"from_cycle": cycle, "to_cycle": cycle + 1,
                      "decision": decision.strip(), "resolved_by": resolved_by.strip(),
                      "resolved_at": timestamp(), "last_report": attempts[-1].get("report")}
        state.setdefault("human_resolutions", []).append(resolution)
        state["current_cycle"] = cycle + 1
        atomic_json(state_path, state)
        return {"cycle": cycle + 1, "attempt": 1, "resolution": resolution}


def require_approval(source):
    try:
        with ledger(source) as (source, _, state):
            cycle = state.get("current_cycle", 1)
            last, _, approval = current_approval(state)
            marker = read_json(source.parent / ".critic-approve")
            require(marker == approval and approval.get("reviewer"), "Invalid .critic-approve")
            require(snapshot(source, Path(approval["context"])) == approval["snapshot"],
                    "Text or context changed; approval is stale")
            require(digest(approval["report"]) == approval["report_sha256"], "The review was changed or lost")
            result = {"approved": True, "source": str(source), "cycle": cycle, "attempt": last["attempt"]}
            if approval is not last:
                result["polish"] = approval["polish"]
            return result
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise GateError(f"DOCX is blocked: inaccessible or corrupt review data: {error}") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("begin", "finish", "cancel", "resolve", "check",
                    "polish-begin", "polish-finish", "polish-cancel"):
        child = commands.add_parser(command)
        child.add_argument("--source", required=True)
        if command == "begin":
            child.add_argument("--context", required=True)
        if command in ("finish", "cancel", "polish-finish", "polish-cancel"):
            child.add_argument("--ticket", required=True)
        if command in ("finish", "polish-finish"):
            child.add_argument("--reviewer", required=True)
        if command == "finish":
            child.add_argument("--verdict", choices=("approve", "revise", "context_error"), required=True)
        if command == "polish-finish":
            child.add_argument("--verdict", choices=("approve", "revise"), required=True)
        if command in ("cancel", "polish-cancel"):
            child.add_argument("--reason", required=True)
        if command == "resolve":
            child.add_argument("--decision", required=True)
            child.add_argument("--resolved-by", default="author")
    args = vars(parser.parse_args())
    command = args.pop("command")
    try:
        result = {"begin": begin, "finish": finish, "cancel": cancel,
                  "resolve": resolve, "check": require_approval,
                  "polish-begin": polish_begin, "polish-finish": polish_finish,
                  "polish-cancel": polish_cancel}[command](**args)
        print(json.dumps(result, ensure_ascii=False))
    except (GateError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
