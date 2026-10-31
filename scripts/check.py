#!/usr/bin/env python3
"""Repo check. Fails the PR when the layout, frontmatter or sibling links drift."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_SKILL_LINES = 100
LONG_SKILLS = {"close-out", "whats-next"}  # predate the cap; detail has not been split out yet
STANDALONE = {"grill-me", "bro"}  # skills that need no sibling mention

errors = []

def err(msg):
    errors.append(msg)

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out

# One plugin ("dp") whose source is the repo root, with skills in skills/<name>/.
market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
plugins = market.get("plugins", [])
if len(plugins) != 1 or plugins[0].get("name") != "dp" or plugins[0].get("source") != "./":
    err("marketplace.json should list exactly one plugin, 'dp', with source './'")
plugin_json = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
if plugin_json.get("name") != "dp":
    err("plugin.json name should be 'dp'")
if "version" in plugin_json or any("version" in p for p in plugins):
    err("the plugin has no version on purpose, so every push to main counts as an update")

skills = {}  # skill name -> text of SKILL.md plus references
sdir = ROOT / "skills"
for skill_dir in sorted(p for p in sdir.iterdir() if p.is_dir()):
    md = skill_dir / "SKILL.md"
    if not md.exists():
        err(f"{skill_dir.relative_to(ROOT)} has no SKILL.md")
        continue
    text = md.read_text()
    fm = frontmatter(text)
    if fm is None:
        err(f"{md.relative_to(ROOT)} has no frontmatter")
        continue
    if not fm.get("name"):
        err(f"{md.relative_to(ROOT)} frontmatter is missing name")
    elif fm["name"] != skill_dir.name:
        err(f"{md.relative_to(ROOT)} name '{fm['name']}' does not match folder '{skill_dir.name}'")
    if not fm.get("description"):
        err(f"{md.relative_to(ROOT)} frontmatter is missing description")
    lines = len(text.splitlines())
    if lines > MAX_SKILL_LINES and skill_dir.name not in LONG_SKILLS:
        err(f"{md.relative_to(ROOT)} is {lines} lines, over the {MAX_SKILL_LINES} line cap. Move detail into references/")
    refs = "".join(p.read_text() for p in skill_dir.glob("references/*.md"))
    skills[skill_dir.name] = text + refs

for name in sorted(skills):
    if name in STANDALONE:
        continue
    mentioned = any(re.search(rf"`{re.escape(name)}`|\({re.escape(name)}\)", t) for other, t in skills.items() if other != name)
    if not mentioned:
        err(f"skill '{name}' is not named by any sibling skill. Add a line under Related skills in a related skill")

if errors:
    print("check failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"check passed: {len(skills)} skills")
