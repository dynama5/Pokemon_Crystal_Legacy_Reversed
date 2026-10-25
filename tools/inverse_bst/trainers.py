"""Rebuild trainer parties for the inverse-BST hack.

Each trainer Pokémon is replaced by the species whose NEW BST is closest to the
original species' OLD BST, preferring a shared type (gym leaders and the Elite
Four prefer their specialty type). Moves are kept where the new species can
learn them and otherwise filled from its level-up learnset.

Usage: python -I trainers.py <repo_root> <pairings.json> <out_parties.asm> <out_report.json>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAIR = json.loads(Path(sys.argv[2]).read_text())
OUT_ASM = Path(sys.argv[3])
OUT_REPORT = Path(sys.argv[4])

LEGENDARIES = {"ARTICUNO", "ZAPDOS", "MOLTRES", "MEWTWO", "MEW", "RAIKOU", "ENTEI",
               "SUICUNE", "LUGIA", "HO_OH", "CELEBI"}

THEMES = {
    "FalknerGroup": "FLYING", "BugsyGroup": "BUG", "WhitneyGroup": "NORMAL",
    "MortyGroup": "GHOST", "ChuckGroup": "FIGHTING", "JasmineGroup": "STEEL",
    "PryceGroup": "ICE", "ClairGroup": "DRAGON", "WillGroup": "PSYCHIC_TYPE",
    "KogaGroup": "POISON", "BrunoGroup": "FIGHTING", "KarenGroup": "DARK",
    "ChampionGroup": "DRAGON", "BrockGroup": "ROCK", "MistyGroup": "WATER",
    "LtSurgeGroup": "ELECTRIC", "ErikaGroup": "GRASS", "JanineGroup": "POISON",
    "SabrinaGroup": "PSYCHIC_TYPE", "BlaineGroup": "FIRE",
}

# Item that only works on one line; dropped if the new species can't use it.
SPECIES_ITEMS = {"LIGHT_BALL": {"PIKACHU"}, "THICK_CLUB": {"CUBONE", "MAROWAK"},
                 "STICK": {"FARFETCH_D"}, "LUCKY_PUNCH": {"CHANSEY"}, "METAL_POWDER": {"DITTO"}}

# ---------- species data ----------
rows = {r["species"]: r for r in PAIR["rows"]}
species_all = [r["species"] for r in sorted(PAIR["rows"], key=lambda r: r["dex"])]

types, old_bst, base_tmhm = {}, {}, {}
for f in (ROOT / "data/pokemon/base_stats").glob("*.asm"):
    txt = f.read_text()
    sp = re.search(r"db (\w+) ;", txt).group(1)
    types[sp] = set(re.search(r"db (\w+), (\w+) ; type", txt).groups())
    nums = re.search(r"db\s+(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\n\s*;\s*hp", txt)
    old_bst[sp] = sum(int(x) for x in nums.groups())
    m = re.search(r"^\s*tmhm (.*)$", txt, re.M)
    base_tmhm[sp] = {x.strip() for x in m.group(1).split(",")} if m and m.group(1).strip() else set()

new_bst = {s: rows[s]["new_bst"] if s in rows else old_bst[s] for s in old_bst}

consts = []
for line in (ROOT / "constants/pokemon_constants.asm").read_text().splitlines():
    m = re.match(r"\s*const (\w+)\s*;\s*([0-9a-fA-F]{2})\b", line)
    if m and len(consts) < 251:
        consts.append(m.group(1))
labels = re.findall(r"dw (\w+)EvosAttacks", (ROOT / "data/pokemon/evos_attacks_pointers.asm").read_text())
label_to_sp = dict(zip(labels, consts))

learnset = {s: [] for s in consts}
old_evos = {s: [] for s in consts}
cur, in_moves = None, False
for line in (ROOT / "data/pokemon/evos_attacks.asm").read_text().splitlines():
    m = re.match(r"\s*(\w+)EvosAttacks:", line)
    if m:
        cur, in_moves = label_to_sp[m.group(1)], False
        continue
    if cur is None:
        continue
    code = line.split(";")[0].strip()
    if code == "db 0":
        in_moves = not in_moves and True if not in_moves else False
        continue
    m = re.match(r"db (EVOLVE_\w+),\s*(.+)", code)
    if m:
        parts = [p.strip() for p in m.group(2).split(",")]
        old_evos[cur].append((m.group(1), parts[0], parts[-1]))
        continue
    m = re.match(r"db (\d+),\s*(\w+)$", code)
    if m and in_moves:
        learnset[cur].append((int(m.group(1)), m.group(2)))

new_evos = {s: [tuple(e) for e in rows[s]["new_evos"]] if s in rows else old_evos[s] for s in consts}

def parent_map(evos):
    p = {}
    for s, lst in evos.items():
        for e in lst:
            p[e[2]] = (s, e)
    return p

old_parent, new_parent = parent_map(old_evos), parent_map(new_evos)

def req_level(s, parent):
    """Lowest level a species can legitimately have through level/stat evolutions."""
    need = 0
    while s in parent:
        s, (method, param, _) = parent[s][0], parent[s][1]
        if method == "EVOLVE_LEVEL":
            need = max(need, int(param))
        elif method == "EVOLVE_STAT":
            need = max(need, int(param.split()[0]))
    return need

def chain_up(s):
    out = [s]
    while s in old_parent:
        s = old_parent[s][0]
        out.append(s)
    return out

def is_final(s):
    return not old_evos[s]

def learnable(s, level):
    moves = set(base_tmhm.get(s, set()))
    for sp in chain_up(s):
        moves |= {mv for lv, mv in learnset[sp] if lv <= level}
    return moves

def levelup_recent(s, level):
    """Moves the species would know from level-up, most recent first (game default)."""
    seen, out = set(), []
    for lv, mv in sorted(learnset[s], key=lambda x: -x[0]):
        if lv <= level and mv not in seen:
            seen.add(mv)
            out.append(mv)
    return out

CANDIDATES = [s for s in consts if s not in LEGENDARIES and s != "UNOWN"]

def pick(orig, level, theme, used):
    """used maps already-chosen replacement -> the original species it replaced."""
    if orig in LEGENDARIES or orig not in old_bst:
        return orig, 0, "kept", 0
    # A leader's deliberate off-type pick (Karen's Gengar) keeps its own typing instead.
    if theme and theme not in types[orig]:
        theme = None
    target = old_bst[orig]
    gap_orig = max(0, req_level(orig, old_parent) - level)
    best = None
    for c in CANDIDATES:
        score = abs(new_bst[c] - target)
        shares = bool(types[c] & types[orig])
        if theme:
            if theme in types[c]:
                pass
            elif shares:
                score += 45
            else:
                score += 80
        elif not shares:
            score += 60
        if is_final(c) != is_final(orig):
            score += 15
        gap = max(0, req_level(c, new_parent) - level)
        score += max(0, gap - gap_orig) * 1.5
        if c in used and used[c] != orig:
            score += 40
        key = (score, abs(new_bst[c] - target), c != orig, consts.index(c))
        if best is None or key < best[0]:
            best = (key, c)
    c = best[1]
    if theme and theme not in types[c]:
        note = "off-theme"
    elif not theme and not (types[c] & types[orig]):
        note = "no shared type"
    else:
        note = ""
    return c, new_bst[c] - target, note, best[0][0]

def new_moves(orig_moves, new_sp, level):
    real = [m for m in orig_moves if m != "NO_MOVE"]
    can = learnable(new_sp, level)
    kept = [m for m in real if m in can]
    fill = [m for m in levelup_recent(new_sp, level) if m not in kept]
    out = kept + fill[: max(0, len(real) - len(kept))]
    out += ["NO_MOVE"] * (4 - len(out))
    return out[:4], len(kept), len(real)

# ---------- parse + rewrite parties ----------
src = (ROOT / "data/trainers/parties.asm").read_text().splitlines()
out = list(src)
report = []

i = 0
group = None
while i < len(src):
    line = src[i]
    g = re.match(r"(\w+Group):", line)
    if g:
        group = g.group(1)
        i += 1
        continue
    h = re.match(r'\s*db "([^"]*)@",\s*(TRAINERTYPE[^;]*)', line)
    if not h:
        i += 1
        continue
    name = h.group(1)
    flags = h.group(2)
    comment = src[i - 1].strip().lstrip(";").strip() if i > 0 and src[i - 1].strip().startswith(";") else name
    has_item = "ITEM" in flags
    has_moves = "MOVES" in flags
    multiline = any(f in flags for f in ("NICKNAME", "DVS", "STAT_EXP"))
    i += 1
    # collect mon records
    mons = []
    while i < len(src) and not re.match(r"\s*db -1", src[i]):
        code = src[i].split(";")[0].strip()
        m = re.match(r"db\s+(\d+),\s*(\w+)(.*)$", code)
        if m:
            rec = {"lvl": int(m.group(1)), "sp": m.group(2), "line": i, "item": None, "moves": None,
                   "item_line": None, "moves_line": None}
            rest = [x.strip() for x in m.group(3).split(",") if x.strip()]
            if not multiline:
                if has_item:
                    rec["item"] = rest.pop(0)
                if has_moves:
                    rec["moves"] = rest[:4]
            mons.append(rec)
        elif multiline and mons and code.startswith("db") and not code.startswith('db "') and not code.startswith("db $") and "PERFECT_DV" not in code and "SHINY" not in code:
            vals = [x.strip() for x in code[2:].split(",")]
            if len(vals) == 4 and has_moves:
                mons[-1]["moves"], mons[-1]["moves_line"] = vals, i
            elif len(vals) == 1 and has_item:
                mons[-1]["item"], mons[-1]["item_line"] = vals[0], i
        i += 1
    theme = THEMES.get(group)
    # Best-fitting slots choose first, so a perfect match isn't pushed out by a weaker one.
    order = sorted(range(len(mons)), key=lambda k: pick(mons[k]["sp"], mons[k]["lvl"], theme, {})[3])
    used, choice = {}, {}
    for k in order:
        choice[k] = pick(mons[k]["sp"], mons[k]["lvl"], theme, used)
        used.setdefault(choice[k][0], mons[k]["sp"])
    team = []
    for k, rec in enumerate(mons):
        sp = rec["sp"]
        new_sp, diff, note, _ = choice[k]
        entry = {"lvl": rec["lvl"], "old": sp, "new": new_sp, "old_bst": old_bst.get(sp),
                 "new_bst": new_bst.get(new_sp), "diff": diff, "note": note}
        # rewrite species on the level line
        out[rec["line"]] = re.sub(r"(db\s+\d+,\s*)" + re.escape(sp) + r"\b", r"\g<1>" + new_sp, out[rec["line"]], count=1)
        if rec["item"] and rec["item"] in SPECIES_ITEMS and new_sp not in SPECIES_ITEMS[rec["item"]]:
            tgt = rec["item_line"] if rec["item_line"] is not None else rec["line"]
            out[tgt] = re.sub(r"\b" + rec["item"] + r"\b", "NO_ITEM", out[tgt], count=1)
            entry["item_note"] = f"{rec['item']} removed"
        if rec["moves"]:
            mv, kept, total = new_moves(rec["moves"], new_sp, rec["lvl"]) if new_sp != sp else (rec["moves"], 4, 4)
            entry["old_moves"], entry["new_moves"] = rec["moves"], mv
            entry["moves_kept"] = f"{kept}/{total}" if new_sp != sp else "all"
            tgt = rec["moves_line"] if rec["moves_line"] is not None else rec["line"]
            old_tail = ", ".join(rec["moves"])
            # replace the move list in place (keep surrounding text/comments)
            pat = r",\s*".join(re.escape(x) for x in rec["moves"])
            new_line, n = re.subn(pat, ", ".join(mv), out[tgt], count=1)
            assert n == 1, (out[tgt], old_tail)
            out[tgt] = new_line
        team.append(entry)
    report.append({"group": group, "name": name, "label": comment, "theme": theme, "team": team})
    i += 1

OUT_ASM.write_text("\n".join(out) + "\n")
OUT_REPORT.write_text(json.dumps(report, indent=1))
total = sum(len(p["team"]) for p in report)
changed = sum(1 for p in report for m in p["team"] if m["new"] != m["old"])
off = sum(1 for p in report for m in p["team"] if m["note"] in ("off-theme", "no shared type"))
print(f"parties {len(report)}, pokemon {total}, replaced {changed}, theme/type breaks {off}")
