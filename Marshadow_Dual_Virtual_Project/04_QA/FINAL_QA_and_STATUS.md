# FINAL QA & STATUS — READY FOR CUBISM
Both PSDs were reopened independently with psd-tools. For every layer the check compared name, group, Z-order, blend,
visibility, offset and pixels against the manifest, then compared the reopened composite against the Fullbody Master.

| Check | Mini | Human |
|---|---|---|
| Result | PASS 16 / WARN 0 / FAIL 0 | PASS 16 / WARN 0 / FAIL 0 |
| Layers (PNG parts) | 109 | 166 |
| Groups | 13 | 18 |
| Hidden by default (toggles) | 62 | 86 |
| Add/Screen FX layers | 18 | 17 |
| Parts with hidden-area restoration (verified occluded area) | 21 | 40 |
| Empty / duplicate / fake / off-canvas / missing file | 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 |
| Composite vs master | identical within tolerance | identical within tolerance |
| Face/body edge crispness parity | PASS (native, no upscale) | PASS |

Details: `01_Mini/qa/MSM_psd_qa.md`, `02_Human/qa/MSH_psd_qa.md`. Toggle sheets: `05_Exports/*_Toggle_QA.png`.

## Known limitations (not machine WARNs)
- The art is procedural vector, not painted (no image-generation tool was available). A paint-over pass is optional.
- The Human turnaround has front and back only. 3/4 and side views were not produced, because the rig is front-view.
- PSDs are 60 MB and 75 MB. They are stored in plain git, under GitHub's 100 MB limit (LFS is not installed).

## Next step
Import each PSD into Live2D Cubism Editor → auto-mesh → deformers → parameters listed in `*/live2d_notes/`.
