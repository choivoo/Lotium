# Hidden Area Validation

복원 포함 레이어: **33개** · 필수 11개 영역 모두 복원 · 기본 포즈에서 노출 없음(복원은 마스터 실루엣 안으로 클립).

| 필수 영역 | 담당 레이어 | 방법 | 결과 |
|---|---|---|---|
| 앞머리 뒤 이마 | Face_Base | 얼굴 타원 전체를 스킨으로 인페인트(앞머리·눈썹 아래 포함) | PASS |
| 머리카락 뒤 얼굴 윤곽 | Face_Base | 타원 하단 14px 측면 확장(AngleX 대응) | PASS |
| 귀 주변 | Ear_R / Ear_L | 이어컵·머리에 가려진 귀를 팔레트로 드로잉 | PASS |
| 눈꺼풀 뒤 안구 | Eye_*_White / Eye_*_Iris | 흰자 개구부 확장, 홍채 윗부분은 아래쪽 미러로 복원 + 하이라이트/동공 인페인트 | PASS |
| 목 뒤 | Neck / Neck_Back | **v002 재작화**: 턱 그림자·외곽선 포함 새 목, 칼라 아래까지 | PASS |
| 재킷 뒤 몸통 | Torso_Restore / Inner_Body / Jacket_Back_Lining | 몸통·이너·재킷 안감 채움 | PASS |
| 팔 뒤 몸통 | Jacket_Side_Under_Arm_R/L | 소매 아래 재킷 측면 채움 | PASS |
| 소매 안 팔 | Arm_R_Under / Arm_L_Under | 어깨→손목 이너 소매 튜브 | PASS |
| 손목 | Arm_*_Under 끝단 + Hand_* | 장갑 아래 손 스킨 복원, 소매 속 손목 연결 | PASS |
| 하의 뒤 다리 | Pants_R / Pants_L / Pants_Waist_Restore | 스트랩·케이블 아래 인페인트, 재킷 밑단 아래 허리 채움 | PASS |
| 액세서리 뒤 의상 | Inner_Body(코어 아래) / Hood_Folded / Headset_Cup_* | 코어·드로스트링 아래 이너, 머리끝 아래 후드, 머리카락 아래 이어컵 | PASS |

## 복원 레이어 목록
- `030_Hair_Headset_Press` — restored:hair under band
- `046_Headset_Cup_L` — FACE+restored under hair
- `047_Headset_Cup_R` — FACE+restored under hair
- `056_Mouth_Teeth_Lower` — restored:drawn
- `058_Mouth_Inside` — FACE+restored
- `059_Brow_L` — restored:drawn (hidden by bangs in master)
- `060_Brow_R` — restored:drawn (hidden by bangs in master)
- `069_Eye_L_Lid_Skin` — restored:drawn lid
- `072_Eye_L_Iris` — FACE+restored under lid
- `073_Eye_L_White` — restored:drawn eyeball
- `078_Eye_R_Lid_Skin` — restored:drawn lid
- `081_Eye_R_Iris` — FACE+restored under lid
- `082_Eye_R_White` — restored:drawn eyeball
- `089_Face_Base` — FACE+restored forehead/eye sockets/sides
- `090_Ear_L` — restored:drawn
- `091_Ear_R` — restored:drawn
- `109_Jacket_Side_Under_Arm_L` — restored:jacket under sleeve
- `110_Jacket_Side_Under_Arm_R` — restored:jacket under sleeve
- `119_Pants_L` — FULLBODY+restored
- `120_Pants_R` — FULLBODY+restored
- `122_Hand_L` — FULLBODY+restored skin under glove
- `124_Hand_R` — FULLBODY+restored skin under glove
- `127_Arm_L_Under` — restored:inner sleeve+wrist
- `128_Arm_R_Under` — restored:inner sleeve+wrist
- `133_Inner_Body` — FULLBODY+restored
- `134_Torso_Restore` — restored
- `135_Pants_Waist_Restore` — restored
- `136_Neck` — FULLBODY+restored
- `137_Neck_Back` — restored
- `139_Jacket_Back_Lining` — restored
- `140_Cable_Port` — drawn
- `141_Hair_Back_Hood` — restored:FACE silhouette
- `143_Hair_Back_Base` — restored:FACE silhouette

## 한계 (정직 기록)
- 복원은 인페인트/팔레트 드로잉 기반: 평탄한 채움이라 큰 회전(±30° 이상)에서는 원화가 수작업 보정 권장.
- 브로우는 마스터에서 앞머리에 가려져 있어 전체를 드로잉으로 복원함.

## v002 (CR-001) 추가 재작화
- `Neck`, `Neck_Back`: 전신 마스터 픽셀 대신 새로 그림 → 이중 턱 제거
- `Inner_Body` 하이넥 상단, `Hood_Folded` 목 뒤 안감: 머리끝에 가려졌던 부분 재작화
- `Face_Base`: 측면 확장은 볼 옆만(턱 아래 번짐 제거)

## v003 (CR-002) — 복원을 실제 재작화로 교체
- 이마·관자놀이·턱선·눈썹·눈 흰자/홍채: Face no-bangs repaint
- 귀·헤드셋 아래 머리: Face no-headset repaint
- 목 뒤 후드 안감·하이넥: Fullbody headless repaint
- 재킷 아래 몸통·팔·허리: Fullbody no-jacket repaint / 소매 아래 재킷 옆판: vest repaint
- 후드 착용: Face hood-up repaint
