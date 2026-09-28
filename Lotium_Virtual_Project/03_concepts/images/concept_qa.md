# Concept QA — Batch 01

생성: Codex CLI 내장 image_generation, 1024×1536, 레퍼런스 없음(텍스트 스펙만). 세 장 모두 스스로 "캐릭터 시트" 레이아웃(메인 전신 + 부위 인셋)으로 출력됨.

| 항목 | A (stream) | B (core) | C (game) |
|---|---|---|---|
| same identity | PASS | PASS | PASS |
| androgynous appearance | PASS | PASS | PASS |
| age impression (15~17) | PASS | PASS | PASS |
| orange hair | PASS | PASS | PASS |
| hair length | WARN 옆머리 약간 짧음 | PASS | PASS |
| eye color (gold/orange) | PASS | PASS | PASS |
| cyan eye ring | WARN 전신에서 식별 어려움 | PASS (인셋 확인) | PASS (인셋 확인) |
| jacket correctness | PASS | PASS | WARN 앞 트임 넓어 칼라 약함 |
| pants correctness | PASS | PASS | PASS |
| shoes correctness | PASS | PASS | PASS |
| headset | PASS | PASS | PASS |
| chest core (마름모) | PASS | PASS | PASS |
| cable tail + 2핀 플러그 | PASS | PASS | PASS |
| Pip | PASS | PASS | PASS |
| spirit ring (3분할) | WARN 머리 위 헤일로 위치 | WARN 머리 위 헤일로 위치 | WARN 머리 위 헤일로 위치 |
| color ratio 40/30/20/10 | PASS | PASS | WARN 검정 비중 높음 |
| silhouette readability | PASS | PASS | PASS |
| Live2D suitability | WARN 3/4 포즈, 손 뻗음 | WARN 3/4 포즈, 손 뻗음 | FAIL 손 주머니·얼굴 옆 |
| originality | PASS | PASS | PASS |
| no Pokémon-copy elements | PASS | PASS | PASS |
| anatomy | PASS | PASS | PASS |
| hands quality | PASS | PASS | WARN 한 손 가려짐 |
| usability | PASS | PASS | WARN |
| **FAIL / WARN** | 0 / 4 | 0 / 2 | 1 / 6 |
| **판정** | APPROVED (보조) | **APPROVED (메인 기준)** | REJECTED (포즈/비율) |

## 결정
- Face/Fullbody Master 기준 = **B**. A의 부드러운 미소, C의 Pip 안테나 끝 발광은 이후 표정/액세서리에 반영.
- Spirit ring: 세 장 모두 머리 위 헤일로로 해석 → 스펙("머리 뒤")과 차이. 천사 헤일로 오해를 막기 위해 Fullbody Master에서 **머리 뒤, 약간 기울어진 3분할 링**으로 지정해 재생성.
- 헤어는 스펙보다 잔가닥이 많지만 지그재그 번개형은 아님 → 허용, Live2D 분리를 위해 마스터에서 덩어리 단순화 지시.
