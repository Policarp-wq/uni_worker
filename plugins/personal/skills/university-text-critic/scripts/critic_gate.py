#!/usr/bin/env python3
"""Local review ledger and hash-bound DOCX gate; Python 3.10+, Linux/WSL or macOS."""

import argparse
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
    print("BLOCKED: Нативный Windows не поддерживается: модуль fcntl недоступен. "
          "Нужно заменить fcntl.flock() на совместимую с Windows блокировку файлов, "
          "сохранив защиту от одновременной записи. До этого проверка критика и допуск DOCX недоступны.",
          file=sys.stderr)
    raise SystemExit(2)

import fcntl


class GateError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"Ожидается JSON-объект: {path}")
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
    require(path.suffix.lower() in suffixes, f"Нужен читаемый текст без конвертации: {path}")
    content = path.read_text(encoding="utf-8")
    require(content.strip() and "\ufffd" not in content and "\x00" not in content,
            f"Пустой или повреждённый текст: {path}")
    return content


def snapshot(source, context):
    text_file(source, (".md",))
    require(context.parent == source.parent, "Контекст должен лежать в папке работы")
    data = read_json(context)
    for key in ("subject", "topic"):
        require(isinstance(data.get(key), str) and data[key].strip(), f"Не заполнено поле {key}")
    requirements = data.get("requirements")
    require(isinstance(requirements, list) and requirements and
            all(isinstance(item, str) and item.strip() for item in requirements),
            "Нужен непустой список requirements из задания")
    previous = data.get("previous")
    require(type(data.get("previous_exists")) is bool and isinstance(previous, list),
            "Укажи previous_exists (true/false) и список previous")
    require(data["previous_exists"] == bool(previous), "previous_exists противоречит previous")
    assignment = data.get("assignment_files", [])
    require(isinstance(assignment, list), "assignment_files должен быть списком")
    files = {str(source): digest(source), str(context): digest(context)}
    for name in previous + assignment:
        require(isinstance(name, str) and name.strip(), "Нужен путь к материалу")
        path = (context.parent / name).resolve(strict=True)
        require(path != source, "Текущая работа не может быть своим исходным материалом")
        text_file(path)
        files[str(path)] = digest(path)
    return files


@contextmanager
def ledger(source, create=False):
    source = Path(source).resolve(strict=True)
    state_path = source.parent / ".critic-state.json"
    lock_path = source.parent / ".critic-lock"
    require(create or lock_path.is_file(), "Нет проверки критика; DOCX запрещён")
    with lock_path.open("a+" if create else "r") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if state_path.exists():
            state = read_json(state_path)
            require(state.get("version") == 1 and state.get("source") == str(source),
                    "Состояние относится к другому источнику; требуется человек")
            attempts = state.get("attempts")
            current_cycle = state.get("current_cycle", 1)
            resolutions = state.get("human_resolutions", [])
            require(isinstance(attempts, list) and type(current_cycle) is int and
                    current_cycle >= 1 and isinstance(resolutions, list) and
                    current_cycle == len(resolutions) + 1,
                    "Повреждена история циклов; требуется человек")
            counts = {}
            previous_cycle = 1
            for item in attempts:
                require(isinstance(item, dict), "Повреждена история попыток; требуется человек")
                cycle = item.get("cycle", 1)
                require(type(cycle) is int and 1 <= cycle <= current_cycle and
                        cycle >= previous_cycle,
                        "Повреждена история циклов; требуется человек")
                counts[cycle] = counts.get(cycle, 0) + 1
                require(counts[cycle] <= 3 and item.get("attempt") == counts[cycle],
                        "Повреждена история попыток; требуется человек")
                previous_cycle = cycle
            require(all(isinstance(item, dict) and item.get("from_cycle") == i and
                        item.get("to_cycle") == i + 1 and isinstance(item.get("decision"), str) and
                        item["decision"].strip()
                        for i, item in enumerate(resolutions, 1)),
                    "Повреждена запись решения автора; требуется человек")
        else:
            require(create, "Нет истории проверки; DOCX запрещён")
            require(not (source.parent / ".critic-approve").exists() and
                    not (source.parent / ".critic").exists(),
                    "Есть следы проверки без истории; требуется человек")
            state = {"version": 1, "source": str(source), "attempts": [],
                     "current_cycle": 1, "human_resolutions": []}
        yield source, state_path, state


def begin(source, context):
    context = Path(context).resolve(strict=True)
    with ledger(source, create=True) as (source, state_path, state):
        files = snapshot(source, context)
        attempts = state["attempts"]
        cycle = state.get("current_cycle", 1)
        cycle_attempts = [item for item in attempts if item.get("cycle", 1) == cycle]
        require(len(cycle_attempts) < 3,
                "HUMAN_REQUIRED: использовано 3/3 в текущем цикле; передай человеку причины и рецензии")
        require(not attempts or attempts[-1].get("verdict") != "pending",
                "Предыдущий критик ещё работает; дождись его или останови и выполни cancel")
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
    require(state["attempts"], "Нет начатой проверки")
    record = state["attempts"][-1]
    require(record.get("ticket") == ticket and record.get("verdict") == "pending",
            "Неверный ticket или попытка уже завершена")
    return record


def finish(source, ticket, reviewer, verdict):
    require(verdict in ("approve", "revise", "context_error"), "Неизвестный вердикт")
    require(isinstance(reviewer, str) and reviewer.strip(), "Нужен ID отдельного критика")
    with ledger(source) as (source, state_path, state):
        record = pending(state, ticket)
        require(snapshot(source, Path(record["context"])) == record["snapshot"],
                "Входы изменились после begin; одобрение запрещено, нужна отмена и новая попытка")
        report = Path(record["report"])
        content = text_file(report, (".md",))
        require(f"Вердикт: {verdict.upper()}" in content,
                "Вердикт в рецензии не совпадает с finish")
        record.update(verdict=verdict, reviewer=reviewer, finished=timestamp(),
                      report_sha256=digest(report))
        atomic_json(state_path, state)
        if verdict == "approve":
            atomic_json(source.parent / ".critic-approve", record)
        return {"verdict": verdict, "cycle": record.get("cycle", 1),
                "attempt": record["attempt"], "report": str(report)}


def cancel(source, ticket, reason):
    require(isinstance(reason, str) and reason.strip(), "Укажи причину отмены")
    with ledger(source) as (_, state_path, state):
        record = pending(state, ticket)
        record.update(verdict="cancelled", reason=reason, finished=timestamp())
        atomic_json(state_path, state)
        return {"verdict": "cancelled", "attempt": record["attempt"],
                "cycle": record.get("cycle", 1)}


def resolve(source, decision, resolved_by="author"):
    require(isinstance(decision, str) and decision.strip(), "Укажи решение автора")
    require(isinstance(resolved_by, str) and resolved_by.strip(), "Укажи, кто разрешил спор")
    with ledger(source) as (_, state_path, state):
        cycle = state.get("current_cycle", 1)
        attempts = [item for item in state["attempts"] if item.get("cycle", 1) == cycle]
        require(len(attempts) == 3 and all(item.get("verdict") != "pending" for item in attempts),
                "HUMAN_REQUIRED: новый цикл можно открыть после завершённых 3/3 попыток")
        require(attempts[-1].get("verdict") in ("revise", "context_error"),
                "Последняя попытка не содержит нерешённого спора; одобренный цикл не сбрасывается")
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
            current_attempts = [item for item in state["attempts"]
                                if item.get("cycle", 1) == cycle]
            require(current_attempts, "В текущем цикле нет завершённой проверки")
            last = current_attempts[-1]
            require(last.get("verdict") == "approve", "Последняя попытка текущего цикла не одобрена")
            marker = read_json(source.parent / ".critic-approve")
            require(marker == last and last.get("reviewer"), "Недействительный .critic-approve")
            require(snapshot(source, Path(last["context"])) == last["snapshot"],
                    "Текст или контекст изменён; допуск устарел")
            require(digest(last["report"]) == last["report_sha256"], "Рецензия изменена или утрачена")
            return {"approved": True, "source": str(source),
                    "cycle": cycle, "attempt": last["attempt"]}
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise GateError(f"DOCX запрещён: недоступные или повреждённые данные проверки: {error}") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("begin", "finish", "cancel", "resolve", "check"):
        child = commands.add_parser(command)
        child.add_argument("--source", required=True)
        if command == "begin":
            child.add_argument("--context", required=True)
        if command in ("finish", "cancel"):
            child.add_argument("--ticket", required=True)
        if command == "finish":
            child.add_argument("--reviewer", required=True)
            child.add_argument("--verdict", choices=("approve", "revise", "context_error"), required=True)
        if command == "cancel":
            child.add_argument("--reason", required=True)
        if command == "resolve":
            child.add_argument("--decision", required=True)
            child.add_argument("--resolved-by", default="author")
    args = vars(parser.parse_args())
    command = args.pop("command")
    try:
        result = {"begin": begin, "finish": finish, "cancel": cancel,
                  "resolve": resolve, "check": require_approval}[command](**args)
        print(json.dumps(result, ensure_ascii=False))
    except (GateError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
