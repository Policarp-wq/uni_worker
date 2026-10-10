"""Check the distributable text files, plugin layout and common privacy leaks."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/personal"
ALLOWED_SUFFIXES = {".md", ".py", ".json", ".yaml"}
PRIVATE = re.compile(
    r"/(?:home|Users)/[\w.-]+/|[A-Z]:\\Users\\[\w.-]+\\"
    r"|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"
    r"|(?:gh[pousr]_|github_pat_|sk-)[A-Za-z0-9_]{20,}"
    r"|^#{1,6}\s+Local personal profile\s*[—-]\s*exclude from export",
    re.MULTILINE,
)


def private_text(content):
    groups = re.findall(r"\b[А-ЯЁ]{2,6}-\d{2}-\d{2}\b", content)
    return bool(PRIVATE.search(content)) or any(g != "ИКБО-00-00" for g in groups)


def inside(base, relative):
    path = (base / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("Path leaves the package")
    return path


def main():
    # Fixture values are fictional and constructed to keep the export scan useful.
    assert private_text("/" + "home" + "/example/file")
    assert private_text("user" + "@" + "example.test")
    assert private_text("ghp_" + "x" * 30)
    assert private_text("ИКБО-" + "12-34")
    assert not private_text("{{STUDENT_GROUP}} ИКБО-00-00")
    try:
        inside(ROOT, "../outside")
    except ValueError:
        pass
    else:
        raise AssertionError("Escaping path accepted")

    errors = []
    files = []
    for path in sorted(ROOT.rglob("*")):
        if any(p in {".git", "__pycache__"} for p in path.relative_to(ROOT).parts):
            continue
        if path.is_symlink():
            errors.append(f"Symlink: {path.relative_to(ROOT)}")
        elif path.is_file():
            files.append(path)
    inventory = ROOT / "FILES.md"
    names = sorted({str(p.relative_to(ROOT)) for p in files} | {"FILES.md"})
    if sys.argv[1:] == ["--write-inventory"]:
        inventory.write_text("# Exported files\n\nExact contents of the portable package. "
                             "Personal local settings are excluded.\n\n" +
                             "\n".join(f"- `{name}`" for name in names) + "\n", encoding="utf-8")
    elif sys.argv[1:]:
        raise SystemExit("Usage: python3 scripts/check.py [--write-inventory]")
    for path in files:
        relative = path.relative_to(ROOT)
        if path.suffix not in ALLOWED_SUFFIXES and path.name != ".gitignore":
            errors.append(f"Unexpected file type: {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        if private_text(content):
            errors.append(f"Potential private data: {relative}")
        if path.suffix == ".json":
            json.loads(content)
        if path.suffix == ".md":
            outside_fences = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", content)
            for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", outside_fences):
                if re.match(r"(?:https?://|#)", href):
                    continue
                target = unquote(href.split("#", 1)[0].strip("<>"))
                try:
                    resolved = inside(path.parent, target)
                    if not resolved.is_file():
                        errors.append(f"Broken link: {relative}: {target}")
                except ValueError:
                    errors.append(f"Escaping link: {relative}")

    manifests = [json.loads((PLUGIN / name).read_text()) for name in
                 ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json")]
    assert len({m["version"] for m in manifests}) == 1, "Plugin versions differ"
    assert all(m["name"] == "personal" for m in manifests)
    codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert codex["name"] == claude["name"] == "agent-kit"
    for source in (codex["plugins"][0]["source"]["path"], claude["plugins"][0]["source"]):
        assert inside(ROOT, source) == PLUGIN
    onboarding = manifests[0]["extensions"]["com.openai"]["onboardingSkill"]
    assert inside(PLUGIN, onboarding).is_file()
    skills = list((PLUGIN / "skills").glob("*/SKILL.md"))
    assert len(skills) == 11, "Expected ten original skills and setup"
    for skill in skills:
        assert re.search(r"^name: " + re.escape(skill.parent.name) + r"$", skill.read_text(), re.M)

    if not inventory.is_file() or re.findall(r"^- `([^`]+)`$", inventory.read_text(), re.M) != names:
        errors.append("Inventory is stale; run with --write-inventory")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(names)} text files, {len(skills)} skills, manifests, links and privacy checks")


if __name__ == "__main__":
    main()
