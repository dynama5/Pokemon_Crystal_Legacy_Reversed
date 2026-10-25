# Inverse BST tools

Scripts that turn Crystal Legacy into the reversed-power hack. Every evolution line swaps its BST curve with its mirror line in the same group (single-stage, 2-stage, 3-stage), ranked by strongest final form. Legendaries are left out.

## What each step changes

| Script | Reads | Writes |
| --- | --- | --- |
| `pairings.py` | an **unmodified** Crystal Legacy checkout | `pairings.json`: line pairings, new stats, new evolution levels |
| `apply.py` | `pairings.json` | base stats, level evolutions, wild encounter tables (grass, surf, fishing, headbutt, swarms, Bug-Catching Contest) |
| `trainers.py` | unmodified checkout + `pairings.json` | `data/trainers/parties.asm` and `trainers.json` |

Rules baked in:

- Each Pokémon keeps its own stat spread, scaled to its partner's BST at the same stage. Stats cap at 255.
- Level evolutions take the partner line's levels when both lines evolve by level. Stone, friendship and trade evolutions keep their method.
- Wild slots: each species takes its partner's spots (same stage). `wild_swap.json` lists the mapping.
- Trainers: each Pokémon becomes one whose new BST matches the original's old BST, sharing a type with it. Gym leaders and the Elite Four keep their specialty type when a close match exists. Moves are kept when learnable, otherwise filled from the level-up list.

## Re-running

Run against a fresh upstream checkout, never on this repo after the changes are in (the scripts check the original stats and will stop).

```sh
git clone https://github.com/cRz-Shadows/Pokemon_Crystal_Legacy /tmp/legacy
python3 tools/inverse_bst/pairings.py /tmp/legacy tools/inverse_bst/pairings.json
git checkout -- data/   # start from Legacy's original data
python3 tools/inverse_bst/apply.py tools/inverse_bst/pairings.json .
python3 tools/inverse_bst/trainers.py /tmp/legacy tools/inverse_bst/pairings.json data/trainers/parties.asm tools/inverse_bst/trainers.json
make
```

## Not swapped yet

Gift Pokémon (starters, Eevee, Dratini, fossils, Togepi egg and so on), static encounters (Sudowoodo, Snorlax, red Gyarados, Lapras, Electrode), and in-game trades still use the original species.
