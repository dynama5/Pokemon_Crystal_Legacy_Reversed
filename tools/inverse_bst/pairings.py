"""Build inverse-BST line pairings from Crystal Legacy source data.

Usage: python -I pairings.py <repo_root> <out_json>
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])

LEGENDARIES = {
    "ARTICUNO", "ZAPDOS", "MOLTRES", "MEWTWO", "MEW",
    "RAIKOU", "ENTEI", "SUICUNE", "LUGIA", "HO_OH", "CELEBI",
}
STAT_NAMES = ["hp", "atk", "def", "spd", "sat", "sdf"]
CAP = 255

# ---------- species order ----------
species = []
for line in (ROOT / "constants/pokemon_constants.asm").read_text().splitlines():
    m = re.match(r"\s*const (\w+)\s*;\s*([0-9a-fA-F]{2})\b", line)
    if m and len(species) < 251:
        species.append(m.group(1))
assert len(species) == 251, len(species)
dex = {s: i + 1 for i, s in enumerate(species)}

# ---------- base stats ----------
stats, types = {}, {}
for f in (ROOT / "data/pokemon/base_stats").glob("*.asm"):
    txt = f.read_text()
    sp = re.search(r"db (\w+) ;", txt).group(1)
    nums = re.search(r"db\s+(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\n\s*;\s*hp", txt)
    stats[sp] = [int(x) for x in nums.groups()]
    t = re.search(r"db (\w+), (\w+) ; type", txt).groups()
    types[sp] = t[0] if t[0] == t[1] else f"{t[0]}/{t[1]}"
assert len(stats) == 251

# ---------- evolutions ----------
labels = re.findall(r"dw (\w+)EvosAttacks", (ROOT / "data/pokemon/evos_attacks_pointers.asm").read_text())
label_to_sp = dict(zip(labels, species))
evos = defaultdict(list)  # species -> [(method, param, target)]
cur = None
for line in (ROOT / "data/pokemon/evos_attacks.asm").read_text().splitlines():
    m = re.match(r"\s*(\w+)EvosAttacks:", line)
    if m:
        cur = label_to_sp[m.group(1)]
        continue
    m = re.match(r"\s*db (EVOLVE_\w+),\s*(.+)", line)
    if m and cur:
        parts = [p.strip() for p in m.group(2).split(";")[0].split(",")]
        method = m.group(1)
        if method == "EVOLVE_STAT":
            param, target = f"{parts[0]} ({parts[1]})", parts[2]
        else:
            param, target = parts[0], parts[1]
        evos[cur].append((method, param, target))

parent = {}
for s, lst in evos.items():
    for _, _, t in lst:
        parent[t] = s

def root_of(s):
    while s in parent:
        s = parent[s]
    return s

def stage_of(s):
    n = 1
    while s in parent:
        s = parent[s]
        n += 1
    return n

lines = defaultdict(list)
for s in species:
    lines[root_of(s)].append(s)

# ---------- wild locations (grass, water, fish, trees) ----------
loc = defaultdict(list)  # species -> [(min_level, place)]
def add(sp, lvl, place):
    loc[sp].append((lvl, place))

for fname in ["johto_grass", "kanto_grass", "johto_water", "kanto_water", "swarm_grass", "swarm_water"]:
    region = "Johto" if "johto" in fname else ("Kanto" if "kanto" in fname else "Swarm")
    kind = "grass" if "grass" in fname else "surf"
    mapname = None
    for line in (ROOT / f"data/wild/{fname}.asm").read_text().splitlines():
        m = re.match(r"\s*def_\w+_wildmons (\w+)", line)
        if m:
            mapname = m.group(1)
            continue
        m = re.match(r"\s*db (\d+), (\w+)\s*$", line.split(";")[0] + "\n")
        if m and mapname and m.group(2) in dex:
            add(m.group(2), int(m.group(1)), f"{mapname} ({kind})")

group = None
for line in (ROOT / "data/wild/fish.asm").read_text().splitlines():
    m = re.match(r"\.(\w+?)_(Old|Good|Super):", line)
    if m:
        group = f"fishing {m.group(1)} {m.group(2)} Rod"
        continue
    m = re.match(r"\s*db\s+[^,]+,\s*(\w+),\s*(\d+)", line)
    if m and group and m.group(1) in dex:
        add(m.group(1), int(m.group(2)), group)

group = None
for line in (ROOT / "data/wild/treemons.asm").read_text().splitlines():
    m = re.match(r"\.(\w+):", line)
    if m:
        group = f"headbutt {m.group(1)}"
        continue
    m = re.match(r"\s*db\s+\d+,\s*(\w+),\s*(\d+)", line)
    if m and group and m.group(1) in dex:
        add(m.group(1), int(m.group(2)), group)

def nice(name):
    return name.replace("_", " ").title()

def where(sp):
    seen, out = set(), []
    for lvl, place in sorted(loc.get(sp, [])):
        if place in seen:
            continue
        seen.add(place)
        out.append(f"{nice(place.split(' (')[0]) if '(' in place else place} Lv{lvl}")
    if not out:
        return "—"
    return "; ".join(out[:3]) + (f" (+{len(out) - 3} more)" if len(out) > 3 else "")

# ---------- line records ----------
def bst(s):
    return sum(stats[s])

line_recs = []
for root, members in lines.items():
    if any(m in LEGENDARIES for m in members):
        continue
    depth = max(stage_of(m) for m in members)
    by_stage = defaultdict(list)
    for m in members:
        by_stage[stage_of(m)].append(m)
    stage_max = {k: max(bst(m) for m in v) for k, v in by_stage.items()}
    final_bst = max(bst(m) for m in members if not evos.get(m))
    line_recs.append({
        "root": root,
        "members": sorted(members, key=lambda m: dex[m]),
        "depth": depth,
        "stage_max": stage_max,
        "final_bst": final_bst,
        "branching": any(len(v) > 1 for v in by_stage.values()),
    })

# ---------- pairing within buckets ----------
pairs = []
partner = {}
rank_info = {}
for depth in (1, 2, 3):
    bucket = [l for l in line_recs if l["depth"] == depth]
    # strongest first; ties broken by dex number
    bucket.sort(key=lambda l: (-l["final_bst"], dex[l["root"]]))
    n = len(bucket)
    for i, l in enumerate(bucket):
        j = n - 1 - i
        partner[l["root"]] = bucket[j]["root"]
        rank_info[l["root"]] = (i + 1, n)

line_by_root = {l["root"]: l for l in line_recs}

def scale(base, target):
    """Scale stats to target BST keeping ratios; largest-remainder rounding, then cap/floor."""
    total = sum(base)
    raw = [b * target / total for b in base]
    fl = [int(x) for x in raw]
    short = target - sum(fl)
    order = sorted(range(6), key=lambda k: -(raw[k] - fl[k]))
    for k in order[:short]:
        fl[k] += 1
    capped = [k for k in range(6) if fl[k] > CAP]
    out = [min(CAP, max(1, v)) for v in fl]
    return out, [STAT_NAMES[k] for k in capped]

rows = []
for l in line_recs:
    p = line_by_root[partner[l["root"]]]
    for m in l["members"]:
        st = stage_of(m)
        # own share of its stage's strongest form, applied to partner's stage strength
        target = round(p["stage_max"][st] * bst(m) / l["stage_max"][st])
        new, capped = scale(stats[m], target)
        rows.append({
            "dex": dex[m],
            "species": m,
            "type": types[m],
            "line_root": l["root"],
            "line_stages": l["depth"],
            "stage": st,
            "rank": rank_info[l["root"]][0],
            "bucket_size": rank_info[l["root"]][1],
            "line_final_bst": l["final_bst"],
            "partner_root": p["root"],
            "swapped": p["root"] != l["root"],
            "old_stats": stats[m],
            "old_bst": bst(m),
            "target_bst": target,
            "new_stats": new,
            "new_bst": sum(new),
            "capped": capped,
            "evos": [list(e) for e in evos.get(m, [])],
            "where": where(m),
        })

# ---------- evolution level swaps ----------
def level_chain(l):
    """Level thresholds per stage transition (stage1->2, stage2->3); None if not a single level evo."""
    out = {}
    for m in l["members"]:
        for method, param, target in evos.get(m, []):
            st = stage_of(m)
            if method == "EVOLVE_LEVEL" and st not in out:
                out[st] = int(param)
            elif method != "EVOLVE_LEVEL":
                out.setdefault(st, None)
    return out

evo_plan = {}
for l in line_recs:
    p = line_by_root[partner[l["root"]]]
    mine, theirs = level_chain(l), level_chain(p)
    plan = {}
    for st, lvl in mine.items():
        if lvl is not None and theirs.get(st) is not None:
            plan[st] = theirs[st]
    evo_plan[l["root"]] = plan

for r in rows:
    plan = evo_plan[r["line_root"]]
    new_evos = []
    for method, param, target in r["evos"]:
        if method == "EVOLVE_LEVEL" and r["stage"] in plan:
            new_evos.append([method, str(plan[r["stage"]]), target])
        else:
            new_evos.append([method, param, target])
    r["new_evos"] = new_evos

legend_rows = [
    {"dex": dex[s], "species": s, "type": types[s], "bst": bst(s)}
    for s in species if s in LEGENDARIES
]

OUT.write_text(json.dumps({"rows": sorted(rows, key=lambda r: r["dex"]), "legendaries": legend_rows}, indent=1))
print("lines:", len(line_recs), {d: sum(1 for l in line_recs if l["depth"] == d) for d in (1, 2, 3)})
print("rows:", len(rows))
