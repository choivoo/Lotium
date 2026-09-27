# PHASE 6 QA Framework

각 생성 이미지마다 이 표를 복사해 `03_concepts/images/<batch>/<ID>_qa.md`로 저장. 판정: PASS / WARN / FAIL.
**승인 조건**: FAIL 0, WARN ≤ 4. `originality` 또는 `no Pokémon-copy` FAIL은 즉시 rejected.

## A. Concept QA (25)
| # | 항목 | 기준 (visual_target_lock.md) | 판정 |
|---|---|---|---|
| 1 | same identity | 다른 후보와 같은 인물로 읽힘 | |
| 2 | youthful neutral face | 15~17세, V라인 둥근 턱 | |
| 3 | androgynous appearance | 여성/성인남성 신호 없음 | |
| 4 | orange hair | #FF8A1F 계열, 끝 앰버 | |
| 5 | correct hair length | 앞: 눈썹 아래 / 옆: 턱선 / 뒤: 목덜미 | |
| 6 | gold/orange eyes | 금빛 방사 홍채 | |
| 7 | cyan eye ring | 얇은 시안 링 | |
| 8 | correct body ratio | 6.5등신 ±0.3 | |
| 9 | correct jacket | 크림 하이넥, 오렌지 패널, 벨 소매 | |
| 10 | black cargo pants | 테이퍼드 | |
| 11 | cream shoes | 검정 두꺼운 솔 | |
| 12 | diamond core | 둥근 모서리 마름모, 원형 아님 | |
| 13 | headset | 슬림, 왼쪽 마이크 | |
| 14 | cable tail | 허리 뒤, 2핀 플러그 | |
| 15 | Pip | 캡슐 1기, 오른쪽 어깨 | |
| 16 | spirit ring | 3분할 | |
| 17 | color ratio | 40/30/20/10 근사 | |
| 18 | silhouette readability | 흑백·256px 판독 | |
| 19 | Live2D suitability | §C 기준 | |
| 20 | originality | 이름 가렸을 때 "로토무 의인화"로 안 읽힘 | |
| 21 | no Pokémon-copy elements | `forbidden_comparison.md` 전부 미해당 | |
| 22 | hands quality | 손가락 5개, 왜곡 없음 | |
| 23 | anatomy | 관절·비율 정상 | |
| 24 | symmetry | 얼굴 좌우 균형 | |
| 25 | production usability | 선·색 경계가 선화화 가능 | |

## B. Face Consistency QA (Face QA Sheet)
패널 간 편차 허용치(얼굴 폭 대비): eye distance ±3%, jaw width ±4%, hairline ±3%, bang placement 동일 그룹, nose height ±3%, mouth position ±3%.

## C. Live2D QA (Fullbody Master 확정 전 필수)
| 항목 | 판정 |
|---|---|
| 앞머리 여러 덩어리 분리 가능 | |
| 옆머리 좌우 분리 가능 | |
| 뒷머리가 얼굴과 별도 | |
| 눈 좌우 독립 | |
| 재킷 좌우 명확 | |
| 팔이 몸통에 붙지 않음 | |
| 손 보임 | |
| 케이블 별도 파츠 가능 | |
| 코어 별도 파츠 | |
| Pip 독립 | |
| spirit ring 별도 | |
| FX 분리 가능 | |

## D. Fullbody Master QA
FACE(Face Master 동일) / HAIR / BODY 6.5 / OUTFIT / COLOR / ACCESSORIES / LIVE2D / ORIGINALITY — 모두 PASS 시 `character_design_lock.md` 상태를 LOCKED로 변경.

## 반복 제한
단계당 첫 배치 최대 3장, 재생성은 FAIL 항목만 프롬프트 수정 후 최대 2회. 탈락은 `03_concepts/images/rejected/` + `rejection_log.md`.
