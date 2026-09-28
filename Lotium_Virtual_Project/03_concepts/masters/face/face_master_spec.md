# Face Master Spec — LOCKED

상태: **LOCKED** · 기준 이미지 `LTM_FACE_MASTER_v001.png` (1254×1254, Codex image_generation, 레퍼런스: LTM_CONCEPT_B_v001)
측정: 원본 픽셀 좌표(수동 격자 측정, ±5px). 비율은 눈높이 얼굴 폭(FW = 415px) 기준 %.

| 요소 | 실측 (px) | FW 대비 | 목표값(r1 스펙) | 판정 |
|---|---|---|---|---|
| face contour | 눈높이 x 425–840, 부드러운 V, 턱끝 둥글게 | 100 | V라인 둥근 턱 | PASS |
| jaw | 턱선 y≈790에서 폭 ≈230 → 턱끝 (632, 840) | 55 | 둥근 턱끝 | PASS |
| cheek volume | 눈 아래 볼 외곽 약간 볼록 | — | 약간 통통 | PASS |
| eye width | 좌 175 / 우 155 (정면 원근 미세 차) | 42 / 37 | 23 | **MASTER 우선** (애니 VTuber 표준 큰 눈) |
| eye height | ≈100 | 24 | — | 기록 |
| eye distance (안쪽 눈꼬리) | ≈95 | 23 | 23 | PASS |
| iris size | 지름 ≈70, 위 눈꺼풀에 살짝 가림 | 17 | 눈 높이 85% | PASS |
| eyebrow thickness | ≈6, 앞머리에 대부분 가려짐 | 1.4 | 2.2 | PASS(가늘게) |
| eyebrow angle | 거의 수평, 바깥 끝 약간 하강 | — | 수평 −5° | PASS |
| nose position | 코끝 y≈680 (눈선 550에서 +130), 점+그림자 | — | 점+짧은 선 | PASS |
| mouth width | 140 (열린 미소) | 34 | 14 (닫힘 기준) | 기록: 기본 파츠는 닫힌 미소 폭 ≈80(19%)으로 제작 |
| default mouth shape | 윗니 살짝 보이는 열린 미소 | — | 작은 열린 미소 | PASS |
| hairline | y≈400 추정(앞머리로 전부 가림) | — | 눈썹 위 | 기록 |
| front bangs | 중앙 가르마 경향 + 눈 사이 가닥 1, 눈썹 아래까지 | — | 7:3 좌가르마 | **MASTER 우선** |
| side hair relationship | 옆머리가 볼 외곽 덮고 턱선 아래까지, 끝 앰버 그라데이션 | — | 턱선 | PASS |
| 시그니처 | 왼눈(캐릭터 기준) 아래 시안 점 2, 오른쪽 옆머리 시안 브리지 | — | 동일 | PASS |

## 확정 규칙
- 스펙과 다른 항목(큰 눈, 가르마)은 **마스터 이미지가 우선**한다(Design Lock 원칙: 이미지 확정 후 이미지가 Source of Truth).
- Face QA Sheet(`LTM_FACE_QA_SHEET_v001.png`) 결과는 아래에 기록.

## Face QA Sheet 결과 (`LTM_FACE_QA_SHEET_v001.png`)
| 검사 | 결과 |
|---|---|
| eye distance | 유지 (PASS) |
| jaw width | 유지 (PASS) |
| hairline | 유지 (PASS) |
| bang placement | 눈 사이 가닥·좌측 시안 스트릭 유지 (PASS) |
| nose height | 유지 (PASS) |
| mouth position | 유지 (PASS) |
판정: 6패널 동일 인물 — FACE LOCK 확정.
