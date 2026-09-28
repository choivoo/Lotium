# PHASE 6 / 7 Status — COMPLETE

## PHASE 6 — Visual Masters (COMPLETE)
이미지 생성 수단: Codex CLI 0.157.1 내장 `image_generation` (ChatGPT 로그인, OPENAI_API_KEY 불필요) · 래퍼 `11_pipeline/tools/codex_gen.py` · 로그 `03_concepts/generation_log.csv`

| 산출물 | 상태 |
|---|---|
| Concept batch 01 (A/B/C) | 생성 · A/B 승인, C 탈락 (`images/concept_qa.md`) |
| Face Master + Face QA Sheet | 승인 · FACE LOCK (`masters/face/`) |
| Fullbody Master | 승인 (`masters/fullbody/`) |
| Turnaround / Accessory / Overclock / Expression Reference | 승인 (`masters/masters_qa.md`) |
| Color Master | 승인 (코드 생성) |
| Character Design Lock | LOCKED (IMAGE) |
| Layer Visual Validation | FINAL v2 (`08_live2d_notes/layer_visual_validation.md`) |

## PHASE 7 — Live2D Parts / PSD (COMPLETE, WARN 4)
| 산출물 | 위치 |
|---|---|
| 파츠 PNG 149 | `08_parts/<category>/NNN_Name.png` |
| PSD | `06_psd_parts/LTM_LIVE2D_MASTER_v003.psd` (3072×4608, 16 그룹, 149 레이어) |
| Manifests | `08_live2d_notes/layer_manifest_final.csv`, `parts_assembly_manifest.json`, `psd_tree_final.md` |
| QA | `parts_qa.md`, `hidden_area_validation.md`, `qa_toggle_preview.png`, `parts_composite_preview.png` |
| 도구 | `11_pipeline/tools/parts/build_parts.py`, `render_preview.py`, `11_pipeline/tools/assemble_psd.py` |

재현: `python3 11_pipeline/tools/parts/build_parts.py` → manifest 생성(상태 문서 참조) → `python3 11_pipeline/tools/assemble_psd.py 08_live2d_notes/parts_assembly_manifest.json 06_psd_parts/LTM_LIVE2D_MASTER_v003.psd`

## 다음: Cubism Rigging
