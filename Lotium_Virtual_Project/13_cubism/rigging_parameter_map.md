# Rigging Parameter Map — Lotium

파라미터 66개 · 원본 `parameters.csv` · 레이어별 연결 `artmesh_plan.csv`

| ID | 이름 | 범위 (min/default/max) | 그룹 | 연결 ArtMesh 수 | 비고 |
|---|---|---|---|---|---|
| `ParamAngleX` | 고개 좌우 | -30 / 0 / 30 | Face | 8 |  |
| `ParamAngleY` | 고개 상하 | -30 / 0 / 30 | Face | 8 |  |
| `ParamAngleZ` | 고개 기울기 | -30 / 0 / 30 | Face | 0 |  |
| `ParamBodyAngleX` | 몸 좌우 | -10 / 0 / 10 | Body | 0 |  |
| `ParamBodyAngleY` | 몸 앞뒤 | -10 / 0 / 10 | Body | 0 |  |
| `ParamBodyAngleZ` | 몸 기울기 | -10 / 0 / 10 | Body | 0 |  |
| `ParamEyeLOpen` | 왼눈 뜨기 | 0 / 1 / 1 | Eyes | 14 |  |
| `ParamEyeLSmile` | 왼눈 웃음 | 0 / 0 / 1 | Eyes | 1 |  |
| `ParamEyeROpen` | 오른눈 뜨기 | 0 / 1 / 1 | Eyes | 10 |  |
| `ParamEyeRSmile` | 오른눈 웃음 | 0 / 0 / 1 | Eyes | 1 |  |
| `ParamEyeBallX` | 눈동자 X | -1 / 0 / 1 | Eyes | 6 |  |
| `ParamEyeBallY` | 눈동자 Y | -1 / 0 / 1 | Eyes | 6 |  |
| `ParamEyeBallForm` | 동공 크기 | -1 / 0 / 1 | Eyes | 0 | 놀람 시 축소 |
| `ParamBrowLY` | L 눈썹 높이 | -1 / 0 / 1 | Brows | 1 |  |
| `ParamBrowLAngle` | L 눈썹 각도 | -1 / 0 / 1 | Brows | 1 |  |
| `ParamBrowLForm` | L 눈썹 모양 | -1 / 0 / 1 | Brows | 1 |  |
| `ParamBrowRY` | R 눈썹 높이 | -1 / 0 / 1 | Brows | 1 |  |
| `ParamBrowRAngle` | R 눈썹 각도 | -1 / 0 / 1 | Brows | 1 |  |
| `ParamBrowRForm` | R 눈썹 모양 | -1 / 0 / 1 | Brows | 1 |  |
| `ParamMouthForm` | 입 모양(-찡그림/+웃음) | -1 / 0 / 1 | Mouth | 10 |  |
| `ParamMouthOpenY` | 입 벌리기 | 0 / 0 / 1 | Mouth | 10 |  |
| `ParamMouthShape` | 입 모음(A/I/U/E/O 보조) | -1 / 0 / 1 | Mouth | 1 | -1=U/O 오므림, +1=I/E 옆으로 |
| `ParamCheek` | 볼 홍조 | 0 / 0 / 1 | Face | 0 |  |
| `ParamBreath` | 호흡 | 0 / 0 / 1 | Body | 13 |  |
| `ParamHairFront` | 앞머리 흔들림 | -1 / 0 / 1 | Physics | 8 |  |
| `ParamHairSide` | 옆머리 흔들림 | -1 / 0 / 1 | Physics | 5 |  |
| `ParamHairBack` | 뒷머리 흔들림 | -1 / 0 / 1 | Physics | 3 |  |
| `ParamAhoge` | 아호게 흔들림 | -1 / 0 / 1 | Physics | 1 |  |
| `ParamDrawstring` | 후드끈 흔들림 | -1 / 0 / 1 | Physics | 2 |  |
| `ParamHem` | 밑단 흔들림 | -1 / 0 / 1 | Physics | 2 |  |
| `ParamSleeveR` | 오른 소매 흔들림 | -1 / 0 / 1 | Physics | 3 |  |
| `ParamSleeveL` | 왼 소매 흔들림 | -1 / 0 / 1 | Physics | 3 |  |
| `ParamStrap` | 스트랩 흔들림 | -1 / 0 / 1 | Physics | 0 |  |
| `ParamCableSwingX` | 케이블 X | -1 / 0 / 1 | Physics | 5 |  |
| `ParamCableSwingY` | 케이블 Y | -1 / 0 / 1 | Physics | 5 |  |
| `ParamPipAntenna` | 핍 안테나 | -1 / 0 / 1 | Physics | 1 |  |
| `ParamRingFloat` | 정령 링 부유 | -1 / 0 / 1 | Physics | 6 |  |
| `ParamMicSwing` | 마이크 흔들림 | -1 / 0 / 1 | Physics | 0 |  |
| `ParamArmRA` | 오른팔 각도 | -1 / 0 / 1 | Body | 8 |  |
| `ParamArmLA` | 왼팔 각도 | -1 / 0 / 1 | Body | 8 |  |
| `ParamPipX` | 핍 X | -1 / 0 / 1 | Accessory | 6 |  |
| `ParamPipY` | 핍 Y | -1 / 0 / 1 | Accessory | 6 |  |
| `ParamRingRotate` | 정령 링 회전 | -1 / 0 / 1 | Accessory | 6 |  |
| `ParamCoreGlow` | 코어 발광 | 0 / 0.5 / 1 | FX | 3 |  |
| `ParamElectricFX` | 전기광 강도(약·중·강) | 0 / 0.5 / 1 | FX | 0 |  |
| `ParamGlitch` | 글리치 | 0 / 0 / 1 | FX | 3 |  |
| `ParamOverclock` | 오버클럭 | 0 / 0 / 1 | FX | 9 |  |
| `ParamHeadset` | 헤드셋 | 0 / 1 / 1 | Toggle | 4 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamMic` | 마이크 | 0 / 1 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamHood` | 후드 | 0 / 0 / 1 | Toggle | 4 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamUI` | UI 패널 | 0 / 1 / 1 | Toggle | 2 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamMobile` | 모바일폼 | 0 / 0 / 1 | Toggle | 2 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamGame` | 게임폼 | 0 / 0 / 1 | Toggle | 2 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamLowBattery` | 배터리 부족 | 0 / 0 / 1 | Toggle | 3 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamPip` | 드론 핍 | 0 / 1 / 1 | Toggle | 5 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamRing` | 정령 링 | 0 / 1 / 1 | Toggle | 5 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamGlove` | 장갑 | 0 / 1 / 1 | Toggle | 2 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamFaceMark` | 얼굴 회로점 | 0 / 1 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamEyeStar` | 눈 반짝 | 0 / 0 / 1 | Toggle | 2 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamTears` | 눈물 | 0 / 0 / 1 | Toggle | 2 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamBlushStrong` | 진한 홍조 | 0 / 0 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamShadowDark` | 얼굴 그늘 | 0 / 0 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamDeadpan` | 무표정 눈 | 0 / 0 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamEmoteHeart` | 이모트 하트 | 0 / 0 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamEmoteSweat` | 이모트 땀 | 0 / 0 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |
| `ParamEmoteAnger` | 이모트 분노 | 0 / 0 / 1 | Toggle | 1 | 0/1 스위치 (파츠 불투명도 키폼 2개) |

## 토글 파라미터 규칙
- 0/1 두 키폼. 대상 ArtMesh의 **불투명도**만 0↔100 (형태 변형 없음).
- `ParamHood=1` → Hood_Up·Hair_Back_Hood 표시, Hood_Folded·Hair_Back_Base 숨김.
- `ParamLowBattery=1` → *_Low·LowBattery_Dim 표시, 일반 배터리·신호 UI 숨김, `ParamCoreGlow` 상한 0.3(표현식에서 설정).
- `ParamMobile=1` → 이어피스·모바일 프레임 표시 + 헤드셋 숨김(헤드셋 ArtMesh 불투명도 키폼에 Mobile 축 추가: Headset=1 & Mobile=0 일 때만 100).
