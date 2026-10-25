"""Apply the inverse-BST swap to a Crystal Legacy checkout.

Reads the swap plan (pairings.json from pairings.py, built from an UNMODIFIED
Crystal Legacy checkout) and rewrites, in the target checkout:
  - data/pokemon/base_stats/*.asm   new stats (same spread, partner's BST)
  - data/pokemon/evos_attacks.asm   level evolutions take the partner's levels
  - data/wild/*.asm                 each species appears where its partner did

Usage: python -I apply.py <pairings.json> <target_repo>
"""
import json
import re
import sys
from pathlib import Path

plan = json.loads(Path(sys.argv[1]).read_text())
target = Path(sys.argv[2])
rows = {r["species"]: r for r in plan["rows"]}

# ---------- base stats ----------
changed = 0
for f in (target / "data/pokemon/base_stats").glob("*.asm"):
    txt = f.read_text()
    sp = re.search(r"db (\w+) ;", txt).group(1)
    if sp not in rows:
        continue
    r = rows[sp]
    pat = re.compile(r"(\tdb)\s+\d+,\s*\d+,\s*\d+,\s*\d+,\s*\d+,\s*\d+(\s*\n\s*;\s*hp)")
    old = [int(x) for x in re.search(r"db\s+(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\n\s*;\s*hp", txt).groups()]
    assert old == r["old_stats"], (sp, old, r["old_stats"])
    new = ", ".join(f"{v:3d}" for v in r["new_stats"])
    txt2, n = pat.subn(lambda m: f"{m.group(1)} {new}{m.group(2)}", txt, count=1)
    assert n == 1, sp
    if txt2 != txt:
        f.write_text(txt2)
        changed += 1
print("base stats files changed:", changed)

# ---------- evolution levels ----------
consts = []
for line in (target / "constants/pokemon_constants.asm").read_text().splitlines():
    m = re.match(r"\s*const (\w+)\s*;\s*([0-9a-fA-F]{2})\b", line)
    if m and len(consts) < 251:
        consts.append(m.group(1))
labels = re.findall(r"dw (\w+)EvosAttacks", (target / "data/pokemon/evos_attacks_pointers.asm").read_text())
label_to_sp = dict(zip(labels, consts))

evo_path = target / "data/pokemon/evos_attacks.asm"
lines = evo_path.read_text().split("\n")
cur, evo_changes = None, 0
for i, line in enumerate(lines):
    m = re.match(r"\s*(\w+)EvosAttacks:", line)
    if m:
        cur = label_to_sp[m.group(1)]
        continue
    m = re.match(r"(\s*db EVOLVE_LEVEL,\s*)(\d+)(,\s*)(\w+)(.*)$", line)
    if m and cur in rows:
        new = {e[2]: e for e in rows[cur]["new_evos"]}
        tgt = m.group(4)
        lvl = new[tgt][1]
        if lvl != m.group(2):
            lines[i] = f"{m.group(1)}{lvl}{m.group(3)}{tgt}{m.group(5)}"
            evo_changes += 1
evo_path.write_text("\n".join(lines))
print("evolution levels changed:", evo_changes)

# ---------- wild encounters ----------
by_line = {}
for r in plan["rows"]:
    by_line.setdefault(r["line_root"], []).append(r)

swap = {}
for r in plan["rows"]:
    partner = by_line[r["partner_root"]]
    same = [p for p in partner if p["stage"] == r["stage"]]
    swap[r["species"]] = max(same, key=lambda p: (p["old_bst"], -p["dex"]))["species"]

WILD = ["johto_grass", "kanto_grass", "johto_water", "kanto_water", "swarm_grass",
        "swarm_water", "fish", "treemons", "bug_contest_mons"]
species_re = re.compile(r"^(\s*db\s+[^;]*?)\b(" + "|".join(sorted(swap, key=len, reverse=True)) + r")\b")
wild_changes = 0
for name in WILD:
    p = target / f"data/wild/{name}.asm"
    out = []
    for line in p.read_text().split("\n"):
        code, sep, comment = line.partition(";")
        m = species_re.match(code)
        if m and swap[m.group(2)] != m.group(2):
            new_sp = swap[m.group(2)]
            rest = code[m.end(2):]
            # keep the next column aligned when the names differ in length
            ws = re.match(r",(\s*)", rest)
            if ws:
                width = max(1, len(ws.group(1)) - (len(new_sp) - len(m.group(2))))
                rest = "," + " " * width + rest[ws.end():]
            code = code[: m.start(2)] + new_sp + rest
            line = code + sep + comment
            wild_changes += 1
        out.append(line)
    p.write_text("\n".join(out))
print("wild encounter slots changed:", wild_changes)

Path(target / "tools/inverse_bst").mkdir(parents=True, exist_ok=True)
(target / "tools/inverse_bst/wild_swap.json").write_text(json.dumps(swap, indent=1, sort_keys=True))
