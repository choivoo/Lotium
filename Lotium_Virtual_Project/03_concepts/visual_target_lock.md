# Visual Target Lock — Character Consistency 기준

Source of Truth: `00_brief/05_final_design/*`. 모든 생성 이미지는 아래 기준으로 QA한다.

| 요소 | LOCK 값 |
|---|---|
| Face shape | 부드러운 V라인, 둥근 턱끝, 폭:높이 1:1.15, 볼 곡선 약간 통통 |
| Eye proportions | 눈 폭 = 얼굴 폭 23%, 눈 사이 간격 = 눈 폭 1개, 눈 높이 = 얼굴 높이 중앙보다 약간 아래 |
| Hairstyle silhouette | 둥근 돔 + 뒤로 흐르는 가닥 3개(좌2·우1), 끝 10%만 1회 꺾임 |
| Hair length | 앞머리: 눈썹 아래 / 옆머리: 턱선 / 뒷머리: 목덜미 덮음, 어깨 위 |
| Body ratio | 6.5등신, 어깨 = 머리 폭 ×1.6, 평평한 상체 |
| Jacket silhouette | 하이넥, 드롭 숄더, 벨 소매(손등 절반), 앞 짧고 뒤 긴 밑단, 옆 슬릿, 접힌 후드 |
| Pants silhouette | 검정 테이퍼드 카고, 무릎 여유, 발목 좁음 |
| Shoe silhouette | 크림 로우~미드컷 테크 스니커, 두꺼운 검정 솔 |
| Headset | 슬림 검정 밴드(머리 위), 둥근 사각 이어컵+시안 링, 왼쪽 붐 마이크 |
| Core | 둥근 모서리 마름모, 가슴 중앙 지퍼 위, 시안 발광 + 게이지 링 |
| Cable | 허리 뒤 포트 → 좌측 뒤 S커브 → 발목 높이, 2핀 플러그 |
| Pip | 납작 캡슐(크림), 귀형 안테나 2(오렌지), 시안 LED 눈 2, 오른쪽 어깨 위 |
| Spirit ring | 머리 뒤 3분할 끊긴 호, 시안 홀로 |
| Color placement | 머리=오렌지 / 재킷=크림 + 오렌지 어깨·옆 패널 / 이너·팬츠·헤드셋=검정 / 신발=크림 |
| Glow placement | 코어, 소매 끝, 지퍼 옆, 이어컵 링, 케이블 전기띠, 머리 이너 라인, 링 (그 외 금지) |

## Prohibited deviations (즉시 FAIL)
- 머리색 변경, 긴 머리/짧은 스파이키 숏, 지그재그 번개머리
- 성인 얼굴·근육·목울대 / 가슴 굴곡·립 메이크업 / SD·아동 비율
- 재킷 색 반전(검정 재킷), 갑옷·기계 부품 과다, 망토, 무기
- 원형/구형 코어, 몬스터볼 형태, 드론 2기 이상, 몸에 붙은 번개 돌기
- 로토무 얼굴·눈·입·몸 실루엣·폼 요소 (`01_reference/forbidden_comparison.md`)

## Revision log
- r2 (PHASE 6 실행 시작): 스펙 변경 없음. 이미지 생성 도구 확보(Codex CLI 내장 image_generation, ChatGPT 로그인) — 모든 생성물은 이 표로 QA.
- 일관성 규칙: Face Master 확정 후 모든 생성 호출에 `-i LTM_FACE_MASTER` / `LTM_FULLBODY_MASTER`를 레퍼런스로 첨부한다.
