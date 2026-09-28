# Masters QA — PHASE 6

생성: Codex CLI 0.157.1 내장 image_generation (ChatGPT 로그인). 모든 마스터는 `LTM_CONCEPT_B_v001` → Face/Fullbody Master를 레퍼런스(-i)로 첨부해 생성.

| 파일 | 크기 | 판정 | 핵심 QA |
|---|---|---|---|
| face/LTM_FACE_MASTER_v001.png | 1254² | **APPROVED** | 정면·대칭, 금빛 홍채+시안 링, 눈 아래 시안 점 2, 헤드셋·붐마이크, 중성 소년형 |
| face/LTM_FACE_QA_SHEET_v001.png | 1536×1024 | **APPROVED** | 정면/3-4 좌/3-4 우 + 미소/장난: 눈 간격·턱폭·헤어라인·앞머리 위치 유지(육안 편차 허용치 내) |
| fullbody/LTM_FULLBODY_MASTER_v001.png | 1024×1536 | **APPROVED** | 정면 A포즈, 팔·몸 분리, 손 노출, 다리 분리, 발 노출, 케이블·Pip·링 분리. WARN: 링이 머리 위 기울어진 헤일로형 |
| turnaround/LTM_TURNAROUND_v001.png | 1536×1024 | **APPROVED** | 정면·3/4·측면·후면 동일 의상, 뒷머리·후드·허리 포트+케이블·헤드밴드·신발 뒤꿈치 확인 |
| palette/LTM_COLOR_MASTER_v001.png | 1800×1960 | **APPROVED** | 코드 생성, 전 색상 HEX |
| accessories/LTM_ACCESSORY_MASTER_v001.png | 1536×1024 | **APPROVED (WARN)** | 헤드셋·코어·케이블+전기띠·Pip 3뷰·링 3호·UI 프레임·배터리 full/low·신호 full/low. WARN: 헤드셋 이어컵에 크림/오렌지 포인트(마스터는 검정) → 파츠는 Face Master 기준 |
| overclock/LTM_OVERCLOCK_MASTER_v001.png | 1024×1536 | **APPROVED** | 동일 헤어·의상, 이중 시안 눈 링, 코어 발광, 스파크·데이터 조각·경고 패널. 악마화/갑옷/오라 없음 |
| expressions/LTM_EXPRESSION_REFERENCE_v001.png | 1254² | **APPROVED** | 16표정(14필수 + sleepy/panic), 동일 얼굴 유지 |

## 오리지널리티 (forbidden_comparison.md 대조)
전 마스터 PASS — 구체 몸체, 오라 속 흰 눈, 번개 팔, 가전 몸체, 화면 얼굴, 몬스터볼 형태, 포켓몬 로고/UI 없음. 인간형 테크웨어 캐릭터로 읽힘.

## 탈락
- LTM_CONCEPT_C_v001 (rejection_log.md)
