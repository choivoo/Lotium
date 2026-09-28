# Lotium_Virtual_Project

로티움(Lotium) — 로토무에서 영감만 받은 오리지널 디지털 전기 정령 버츄얼 캐릭터 제작 프로젝트.

## 진행 상태
- [x] PHASE 1: 프로젝트 개요 → `00_brief/01_project_overview.md`
- [x] PHASE 2: 캐릭터 컨셉 → `00_brief/02_character_concept.md`
- [x] PHASE 3: 비주얼 아트 디렉션 → `00_brief/03_visual_direction/`
- [x] PHASE 4: 전신 디자인 3안 + 병합 → `03_concepts/proposals/`
- [x] PHASE 5: 최종 디자인 사양 + 프롬프트 → `00_brief/05_final_design/`, `02_prompts/`
- [x] 설계 문서(원 요청 6~8): PSD 구조 / 134레이어 / 14표정 / 토글·단축키·방송 세트 → `08_live2d_notes/`
- [x] 설계 문서(원 요청 9~13): 파이프라인 / 작업 순서 / 폴더 구조 / 체크리스트 → `11_pipeline/`, `10_checklists/`
- [x] PHASE 6: Visual Masters + Character Design Lock (Codex image_generation) → `03_concepts/masters/`, `03_concepts/PHASE6_STATUS.md`
- [x] PHASE 7: Live2D 파츠 149 PNG + `06_psd_parts/LTM_LIVE2D_MASTER_v001.psd` → `08_parts/`, `08_live2d_notes/`
- [ ] **다음: Cubism Rigging** (파라미터·물리·표정·토글 = `08_live2d_notes/toggles_hotkeys.md`, `expressions.md`, `layer_manifest_final.csv`의 parameter 열)

## 폴더
| 폴더 | 용도 |
|---|---|
| 00_brief | 기획·아트 디렉션·최종 사양 |
| 01_reference | 레퍼런스 보드 (mood/color/silhouette/techwear/effects) |
| 02_prompts | 이미지 생성 프롬프트 |
| 03_concepts | 디자인 3안·병합안·생성 결과 |
| 04_lineart | 선화 |
| 05_render | 채색 |
| 06_psd_parts | 파츠 분리 PSD |
| 07_export | 썸네일/프로필/쇼츠 출력 |
| 08_parts | Live2D 파츠 PNG (카테고리별) |
| 08_live2d_notes | PSD 트리·최종 manifest·QA·표정·토글 |
| 09_versions | 버전 스냅샷·수정 요청 |
| 10_checklists | 검수 체크리스트 |
| 11_pipeline | 제작 파이프라인·작업 순서·폴더 구조 |

## 파일 네이밍
`LTM_<단계>_<내용>_v<번호>.<확장자>` 예: `LTM_concept_front_v003.png`

## 최종 산출물 (리깅 직전 패키지)
- `06_psd_parts/LTM_LIVE2D_MASTER_v001.psd` — 149 레이어 / 16 그룹 / 3072×4608
- `08_parts/` — 동일 캔버스 좌표 투명 PNG 149
- `08_live2d_notes/layer_manifest_final.csv` · `parts_assembly_manifest.json` · `psd_tree_final.md`
- `08_live2d_notes/parts_qa.md` · `hidden_area_validation.md` · `layer_visual_validation.md` · `qa_toggle_preview.png`
- `03_concepts/masters/` — Face / Fullbody / Turnaround / Color / Accessory / Overclock / Expression 마스터
- `00_brief/05_final_design/character_design_lock.md` — LOCKED
