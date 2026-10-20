#!/usr/bin/env python3
"""Prose metrics, Russian style lint and the mandatory compression gate before critic review."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

MIN_REDUCTION = 0.10
REGROWTH = 0.05
SOFT_SENTENCE = 25
HARD_SENTENCE = 40
PARAGRAPH_SENTENCES = 6

WORD = re.compile(r"[A-Za-zА-Яа-яЁё0-9][A-Za-zА-Яа-яЁё0-9_\-]*")
CAPTION = re.compile(r"^(?:Таблица|Рисунок|Листинг)\b")
ABBREVIATIONS = re.compile(r"\b(?:т\. ?е|т\. ?д|т\. ?п|т\. ?к|и др|см|рис|табл|стр|гл|п|пр|др|им|г|ч|мин|с)\.", re.I)

HARD_RULES = {
    "stock-phrase": re.compile(
        r"следует отметить|стоит отметить|необходимо отметить|важно (?:подчеркнуть|отметить)|"
        r"в рамках данной|данн(?:ая|ой) (?:работ|практическ)|играет (?:ключевую|важную) роль|"
        r"имеет (?:огромное|большое|важное) значение|обеспечивает (?:высокую )?эффективность|"
        r"надеемся|как (?:уже )?было (?:сказано|отмечено) (?:выше|ранее)", re.I),
    "em-dash": re.compile("—"),
}

SOFT_RULES = {
    "nominalization": re.compile(
        r"\bосуществля\w*|\bпроизвод(?:ится|ятся|ился)\s+\w+(?:ние|ка)\b|"
        r"\bвыполня(?:ется|ются)\s+\w+(?:ние|ка)\b|\bпроизведен\w*\s+\w+(?:ние|ка)\b|"
        r"\bпутём\s+\w+ния\b|\bявляется\b|\bявляются\b", re.I),
    "process-narration": re.compile(
        r"\bскрипт\w*|\bисходник\w*|\bсгенерир\w*|\bвыведен\w* из\b|\bне стал[аио]?\b|"
        r"\.(?:drawio|archimate|py|ipynb)\b|\bв (?:этой|данной) работе\b", re.I),
    "hedge-stack": re.compile(
        r"\b(?:может|могут|возможно|вероятно|потенциально)\b[^.!?]{0,40}"
        r"\b(?:может|могут|возможно|вероятно|потенциально|способствовать|позволить)\b", re.I),
    "number-word": re.compile(
        r"\b(?:два|две|двух|три|трёх|трех|четыре|четырёх|пять|пяти|шесть|шести|семь|семи|"
        r"восемь|восьми|девять|девяти|десять|десяти)\b", re.I),
    "semicolon": re.compile(r";"),
}


class GateError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, data):
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def paragraphs(text):
    """Prose blocks: no tables, code, display formulas, images, headings or captions."""
    text = re.sub(r"(?ms)^```.*?^```[ \t]*$", "", text)
    text = re.sub(r"(?s)\$\$.*?\$\$", "", text)
    blocks = []
    for block in re.split(r"\n[ \t]*\n", text):
        lines = []
        for line in block.splitlines():
            stripped = line.strip()
            if (not stripped or stripped.startswith(("|", "#", "![", "<")) or CAPTION.match(stripped)):
                continue
            lines.append(stripped)
        if not lines:
            continue
        items = [lines] if not lines[0].startswith(("- ", "* ", "+ ")) and not re.match(r"\d+[.)] ", lines[0]) else [[l] for l in lines]
        for item in items:
            prose = " ".join(re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", l) for l in item)
            prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", prose)
            prose = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", prose)
            prose = re.sub(r"\$[^$\n]*\$", " ", prose)
            prose = re.sub(r"`[^`]*`", " code ", prose)
            prose = prose.replace("\\_", "_").replace("\\*", "*")
            if WORD.search(prose):
                blocks.append(prose.strip())
    return blocks


def sentences(paragraph):
    masked = ABBREVIATIONS.sub(lambda m: m.group(0).replace(".", "\x00"), paragraph)
    parts = re.split(r"(?<=[.!?])\s+(?=[«\"(]?[A-ZА-ЯЁ0-9])", masked)
    return [p.replace("\x00", ".").strip() for p in parts if WORD.search(p)]


def words(text):
    return WORD.findall(text)


def analyze(text):
    blocks = paragraphs(text)
    findings = []
    total = 0
    for number, block in enumerate(blocks, 1):
        total += len(words(block))
        sents = sentences(block)
        if len(sents) > PARAGRAPH_SENTENCES:
            findings.append({"rule": "long-paragraph", "hard": False, "paragraph": number,
                             "text": block[:120], "detail": f"{len(sents)} предложений"})
        for sentence in sents:
            count = len(words(sentence))
            if count > SOFT_SENTENCE:
                findings.append({"rule": "long-sentence", "hard": count > HARD_SENTENCE,
                                 "paragraph": number, "text": sentence[:160],
                                 "detail": f"{count} слов"})
        for name, pattern in HARD_RULES.items():
            for match in pattern.finditer(block):
                findings.append({"rule": name, "hard": True, "paragraph": number,
                                 "text": block[max(0, match.start() - 40):match.end() + 40]})
        for name, pattern in SOFT_RULES.items():
            for match in pattern.finditer(block):
                findings.append({"rule": name, "hard": False, "paragraph": number,
                                 "text": block[max(0, match.start() - 40):match.end() + 40]})
    return {"prose_words": total, "paragraphs": len(blocks),
            "hard": sum(f["hard"] for f in findings),
            "soft": sum(not f["hard"] for f in findings), "findings": findings}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(source):
    source = Path(source).resolve(strict=True)
    require(source.suffix.lower() == ".md", f"Markdown source is required: {source}")
    state_path = source.parent / ".compress-state.json"
    state = None
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        require(isinstance(state, dict) and state.get("version") == 1 and
                state.get("source") == str(source) and isinstance(state.get("rounds"), list),
                "Compression state belongs to another source or is corrupt; human intervention is required")
    return source, state_path, state


def measure(source):
    return analyze(Path(source).read_text(encoding="utf-8"))


def baseline(source):
    source, state_path, state = load(source)
    state = state or {"version": 1, "source": str(source), "rounds": []}
    rounds = state["rounds"]
    require(not rounds or rounds[-1].get("result") is not None,
            "A compression round is already open; a baseline cannot be re-recorded before compress")
    report = measure(source)
    require(report["prose_words"] > 0, "No prose to measure")
    rounds.append({"round": len(rounds) + 1, "baseline": {"sha256": digest(source),
                   "prose_words": report["prose_words"], "at": timestamp()}, "result": None})
    atomic_json(state_path, state)
    return {"round": len(rounds), "prose_words": report["prose_words"]}


def compress(source, minimum=MIN_REDUCTION, waive=None):
    require(minimum >= MIN_REDUCTION, f"The required reduction cannot be lower than {MIN_REDUCTION:.0%}")
    source, state_path, state = load(source)
    require(state and state["rounds"] and state["rounds"][-1].get("result") is None,
            "No open compression round; run baseline on the uncompressed final version first")
    current = state["rounds"][-1]
    report = measure(source)
    before = current["baseline"]["prose_words"]
    after = report["prose_words"]
    reduction = (before - after) / before
    outcome = {"before": before, "after": after, "reduction": round(reduction, 4),
               "required": minimum, "hard_findings": report["hard"]}
    passed = reduction >= minimum and report["hard"] == 0
    if not passed and not (waive and waive.strip()):
        problems = []
        if reduction < minimum:
            problems.append(f"prose reduced by {reduction:.1%} ({before} -> {after} words), "
                            f"{minimum:.0%} required")
        if report["hard"]:
            problems.append(f"{report['hard']} hard lint findings remain (run lint)")
        raise GateError("COMPRESSION_REQUIRED: " + "; ".join(problems))
    current["result"] = {**outcome, "sha256": digest(source), "at": timestamp(),
                         "waiver": waive.strip() if not passed else None}
    atomic_json(state_path, state)
    atomic_json(source.parent / ".compress-approve", {"source": str(source), **current})
    return current


def require_compression(source):
    """Called by critic_gate.begin: an approved round exists and the text has not regrown."""
    source, _, state = load(source)
    require(state and state["rounds"], "COMPRESSION_REQUIRED: no compression round; run baseline and compress before review")
    approved = [r for r in state["rounds"] if r.get("result")]
    require(approved and state["rounds"][-1].get("result"),
            "COMPRESSION_REQUIRED: the latest compression round is open; run compress")
    marker_path = source.parent / ".compress-approve"
    require(marker_path.is_file(), "COMPRESSION_REQUIRED: .compress-approve is missing")
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    last = state["rounds"][-1]
    require(marker == {"source": str(source), **last}, "Invalid .compress-approve")
    limit = int(last["result"]["after"] * (1 + REGROWTH))
    current = measure(source)["prose_words"]
    require(current <= limit,
            f"COMPRESSION_REQUIRED: prose grew to {current} words after compression "
            f"({last['result']['after']}, limit {limit}); run a new baseline and compress round")
    return {"compressed": True, "round": last["round"], "prose_words": current, "limit": limit}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("lint", "baseline", "compress", "check"):
        child = commands.add_parser(command)
        child.add_argument("--source", required=True)
        if command == "compress":
            child.add_argument("--min", type=float, default=MIN_REDUCTION, dest="minimum")
            child.add_argument("--waive", help="Explicit human decision accepting a smaller reduction")
    args = vars(parser.parse_args())
    command = args.pop("command")
    try:
        result = {"lint": measure, "baseline": baseline, "compress": compress,
                  "check": require_compression}[command](**args)
        print(json.dumps(result, ensure_ascii=False, indent=1))
        if command == "lint" and result["hard"]:
            return 1
    except (GateError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
