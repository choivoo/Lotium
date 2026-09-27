# Codex CLI / Claude 제작 파이프라인

## 1. 전체 흐름
```
기획(00_brief) → 프롬프트(02_prompts) → 레퍼런스(01_reference) → 생성/러프(03_concepts)
→ 정제·선화(04_lineart) → 채색(05_render) → 파츠 분리(06_psd_parts) → PSD 정리 → 리깅 노트(08) → 출력(07) → 스냅샷(09)
```
- 문서·표·CSV는 CLI가 관리(텍스트 → diff 가능, 스마트폰에서도 열람).
- 이미지 바이너리는 `03~07` 폴더에 저장하되 큰 PSD는 Git LFS 사용 권장(`*.psd`, `*.png` 추적).

## 2. CLI가 관리하는 파일 종류
| 종류 | 파일 | 역할 |
|---|---|---|
| 아트 디렉션 | `00_brief/03_visual_direction/*.md` | 스타일 기준 |
| 최종 사양 | `00_brief/05_final_design/*.md` | 디자인 확정값 |
| 프롬프트 | `02_prompts/*.md` | 생성 입력 |
| 레이어 설계 | `08_live2d_notes/psd_layer_structure.md`, `layer_list.csv` | PSD 기준 |
| 파츠 리스트 | `layer_list.csv` (진행 상태 열 추가 가능) | 진행 추적 |
| 체크리스트 | `10_checklists/*.md` | 검수 |
| 수정 요청 | `09_versions/change_requests/CR-NNN.md` | 피드백 |
| 생성 로그 | `03_concepts/generation_log.csv` | 프롬프트·시드·결과 기록 |

## 3. 버전 관리
- 브랜치: 작업 단위(`claude/<topic>`), 마일스톤마다 태그 `v0.1-brief`, `v0.2-concept`, `v0.3-lineart`, `v0.4-render`, `v0.5-psd`, `v1.0-release`.
- 이미지 버전: 파일명 `_vNNN` 증가, 덮어쓰기 금지. 채택본은 `09_versions/<태그>/`에 복사.
- 커밋 메시지: `[PHASE n] 무엇을 왜` (예: `[P6] 표정 대체 레이어 12개 추가`).

## 4. 네이밍
- 폴더: `NN_lowercase` (두 자리 번호 + 소문자 영문).
- 파일: `LTM_<stage>_<subject>_<variant>_vNNN.<ext>`
  - stage: brief / ref / prompt / concept / line / render / psd / export / rig
  - 예: `LTM_concept_front_B_v004.png`, `LTM_psd_main_v012.psd`, `LTM_export_thumb_overclock_v001.png`
- 레퍼런스: `REF_<category>_<source-short>_NNN.jpg` + 같은 이름 `.md` 메모.
- PSD 레이어: `NNN_Group_Part_Side_State`.

## 5. 수정 요청 템플릿 (`09_versions/change_requests/CR-NNN.md`)
```
# CR-NNN: <제목>
- 대상 파일: 
- 대상 레이어/부위: 
- 현재 문제: 
- 원하는 결과: 
- 기준 문서: (예: hair_spec.md §앞머리)
- 우선순위: 높음 / 중간 / 낮음
- 참고 이미지: 
- 완료 조건: 
- 상태: 요청 / 진행 / 검수 / 완료
```

## 6. Claude(Codex CLI)에게 시킬 단계별 작업
1. `00_brief` 읽고 요구사항 요약·모순 점검 → 수정 커밋.
2. 레퍼런스 카테고리별 수집 기준표 작성(`01_reference/README.md`).
3. 최종 사양 기반으로 프롬프트 변형 생성(각도/표정/폼) → `02_prompts/variants/`.
4. 생성 결과 파일을 규칙대로 리네임·분류, `generation_log.csv` 기록.
5. 선택안 검수: `originality_rules.md` 체크 결과 문서화.
6. `layer_list.csv`에 status 열 추가 → 파츠별 진행률 집계 스크립트 실행.
7. PSD 내보내기 후 레이어명 검증 스크립트(psd-tools 사용)로 CSV와 대조.
8. 표정/토글 설정값을 `expressions.md`·`toggles_hotkeys.md`와 대조.
9. 체크리스트 자동 리포트 생성 → 미통과 항목 CR 생성.
10. 마일스톤 태그 + `09_versions` 스냅샷.

## 7. 레퍼런스 수집 기준
| 카테고리 | 고르는 기준 | 가져올 것 |
|---|---|---|
| mood | 밝은 테크 무드, 청량한 전기 느낌 | 분위기·조명 |
| color | 주황+시안 보색 조합, 크림 쉘 제품 사진 | 비율·명도 |
| silhouette | 오버사이즈 쉘, 하이넥, 벨 소매 | 외곽 형태 |
| techwear | 실제 테크웨어 제품(스트랩·패널·지퍼) | 구조·봉제 |
| effects | 회로 기판, 홀로그램, 스캔라인, glitch 아트 | 패턴 원리 |

## 8. 저작권 원칙
- 레퍼런스는 **보기만** 한다: 트레이싱, 부분 오려 붙이기, 이미지 투 이미지 입력 금지(자기 작업물 제외).
- 한 레퍼런스에서 1개 요소만 차용(색 or 실루엣 or 재질). 2개 이상 겹치면 제외.
- 포켓몬/로토무 공식 이미지는 **레퍼런스 보드에 넣지 않는다**(비교 검수용으로만 별도, 비공개).
- 출처 URL·차용 요소를 `.md` 메모에 기록.

## 9. 레퍼런스 보드 작성법
- 카테고리별 3×3 그리드(9장) 이하, 각 이미지 하단에 "차용: ___ / 배제: ___" 캡션.
- 보드 1장 = `01_reference/<category>/BOARD_<category>_vNNN.png` + `BOARD_<category>.md`.

## 10. 최종 오리지널화
1. 레퍼런스를 닫고 사양 문서만 보고 러프.
2. 시그니처 3요소(회로 앤젤링, 마름모 코어, 케이블+핍) 적용 확인.
3. 흑백 실루엣으로 로토무·기존 캐릭터와 비교 → 겹치면 수정.
4. 생성 이미지는 레퍼런스로만 쓰고 최종 선화는 직접 작화/재작성.
