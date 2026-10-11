#!/usr/bin/env python3
"""Guard explicit document/audio paths in shell commands and file reads; never execute them."""

import json
from pathlib import Path
import re
import shlex
import sys


DOCUMENTS = ("pdf", "doc", "docx", "pptx")
AUDIO = ("mp3", "wav", "m4a", "m4b", "aac", "flac", "ogg", "oga", "opus", "aif", "aiff", "wma", "amr")


def paths_with(extensions):
    return re.compile(r"(?i)(?:^|[^a-z0-9_])[^\s'\"|;&()]+\.(?:" + "|".join(extensions) + r")(?:$|[^a-z0-9_])")


DOCUMENT_PATH = paths_with(DOCUMENTS)
AUDIO_PATH = paths_with(AUDIO)
READER = re.compile(
    r"(?:^|[|;&\n]\s*)(?:\$\{?\w+\}?(?=\s)|(?:[\w./-]+/)?"
    r"(?:cat|bat|less|more|sed|awk|grep|rg|head|tail|strings|od|xxd|hexdump|"
    r"perl|python(?:[0-9.]*)?|ruby|node|php|jq|yq|pdftotext|pandoc|unzip|7z))"
    r"(?:\s|$)", re.IGNORECASE,
)
QUOTED = r"(?:'[^'\n]*'|\"[^\"\n]*\")"
WRITE_CALL = re.compile(
    rf"(?:\.save\(\s*{QUOTED}\s*\)|"
    rf"\bopen\(\s*{QUOTED}\s*,\s*(?:mode\s*=\s*)?['\"][wa][bt+]*['\"]\s*\)|"
    rf"\bPath\(\s*{QUOTED}\s*\)\.(?:write_text|write_bytes)\()"
)
OUTPUT = re.compile(rf">{{1,2}}\s*(?:{QUOTED}|[^\s;&|<>]+)")


def existing_markdown(source, cwd):
    path = Path(source)
    if not path.is_absolute():
        path = Path(cwd) / path
    md = path.with_suffix(".md")
    try:
        if md.read_text(encoding="utf-8").strip():
            return md
    except (OSError, UnicodeError):
        pass
    return None


def check(command, cwd="."):
    if not isinstance(command, str):
        return None
    # Only a standalone filename listing is exempt, never a whole command chain.
    if re.fullmatch(r"\s*(?:[\w./-]+/)?rg\s+[^|;&\n<>`$]*--files(?:\s+[^|;&\n<>`$]*)?\s*", command):
        return None
    if AUDIO_PATH.search(command):
        return "Audio reading, transcription and conversion are prohibited; do not invoke markitdown or another processor on audio."

    # Ignore explicit write destinations, while retaining other paths in the command.
    reading = OUTPUT.sub("", WRITE_CALL.sub("", command))
    if DOCUMENT_PATH.search(reading) and READER.search(reading):
        return "Direct reading of PDF, DOC, DOCX and PPTX is blocked. Read an existing same-basename .md rendition; otherwise convert with markitdown, validate it, then read Markdown."

    try:
        args = shlex.split(command)
    except ValueError:
        return None
    if args and Path(args[0]).name == "markitdown":
        for arg in args[1:]:
            if Path(arg).suffix.lower().lstrip(".") in DOCUMENTS:
                cached = existing_markdown(arg, cwd)
                if cached:
                    return f"Markdown already exists: {cached}. Read it directly instead of converting the source again."
                break
    return None


def check_read(path, cwd="."):
    if not isinstance(path, str):
        return None
    suffix = Path(path).suffix.lower().lstrip(".")
    if suffix in AUDIO:
        return "Audio reading, transcription and conversion are prohibited."
    if suffix in DOCUMENTS:
        cached = existing_markdown(path, cwd)
        if cached:
            return f"Direct reading of PDF, DOC, DOCX and PPTX is blocked. Read the existing Markdown instead: {cached}"
        return "Direct reading of PDF, DOC, DOCX and PPTX is blocked. Convert with markitdown (personal:file-to-markdown), validate the result, then read the Markdown."
    return None


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    tool_input = event.get("tool_input", {})
    cwd = tool_input.get("workdir", tool_input.get("cwd", event.get("cwd", ".")))
    if event.get("tool_name") == "Read":
        reason = check_read(tool_input.get("file_path"), cwd)
    else:
        reason = check(tool_input.get("command", tool_input.get("cmd", "")), cwd)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))


if __name__ == "__main__":
    main()
