# Marshadow Dual Virtual Project

This project contains two Live2D PSDs. Each one can be imported and rigged in Cubism on its own.

| | PSD | Canvas | Layers | Groups | QA |
|---|---|---|---|---|---|
| **A — Mini Marshadow** (mascot, NORMAL ↔ SHADOW FIGHTING) | `01_Mini/psd/Marshadow_Mini_Live2D_Master_v001.psd` | 3000×3600 | 109 | 13 | PASS 16 / WARN 0 / FAIL 0 |
| **B — KAGETSU 影月** (human, NORMAL / SHADOW / COMBAT / OVERDRIVE + hood) | `02_Human/psd/Marshadow_Human_Live2D_Master_v001.psd` | 3072×4608 | 166 | 18 | PASS 16 / WARN 0 / FAIL 0 |

## How the art was made (important)
This container had **no Codex CLI and no image-generation API**, and no earlier Lotium scripts existed in this repo.
So every image here comes from a **procedural vector part engine** (`03_Shared_Tools/partkit.py`):
- Each Live2D part is authored as a complete shape: fills, clipped shading, line art and glows.
- Each part is rendered at 2–3× supersampling into its own transparent PNG, with canvas offsets.
- Because each part is drawn whole, the areas hidden behind other parts are restored by construction.
- The Fullbody Master is the composite of the default-visible parts, so composite and master match exactly.
- Everything is rendered at native resolution with no upscaling, so the Lotium body-blur problem cannot recur.

The trade-off is style: the result is clean flat-vector anime, not painted illustration. You can paint over any
part PNG and re-run the assembly while keeping the manifest coordinates.

## Rebuild
```
pip install psd-tools numpy pillow
cd 03_Shared_Tools
python build_model.py ../01_Mini/mini_model.py     # ~4 min
python build_model.py ../02_Human/human_model.py   # ~5 min
```
Each build runs: parts → PNGs → `layer_manifest_final.csv` / `parts_assembly_manifest.json` / `psd_tree_final.md`
→ state previews and master sheets → PSD → independent reopen verification (`qa/*_psd_qa.md`).

## Layout
- `01_Mini/`, `02_Human/`: `brief/ masters/ parts/<group>/ psd/ qa/ live2d_notes/` plus the model definition
- `03_Shared_Tools/`: `partkit.py` (part engine), `build_model.py` (pipeline), `assemble_psd.py` (PSD writer + QA)
- `04_QA/`: combined QA report · `05_Exports/`: toggle QA sheets and mode previews

## IP note
Model A copies the Pokémon Marshadow silhouette (fan art, made on request). Use it for personal or fan purposes only,
not for commercial streaming or merchandise. Model B (KAGETSU) is an original character; it borrows only the general
mood (shadow, spectral green, hood, fighter) and no Pokémon shapes, logos or names.
