# 단축키/토글 레이어 설계

## 1. 토글 목록
| 토글 | 파라미터 | 레이어 | 사용 상황 |
|---|---|---|---|
| 헤드셋 on/off | Tgl_Headset | 032~036 | off: 감성/수면/노래 방송, 후드 착용 시 |
| 후드 on/off | Tgl_Hood | 116, 117, 125 | 새벽 방송, 추운 날, 삐짐 연출 |
| 전기광 약/중/강 | Glow_Level (0/0.5/1) | 035, 091, 097, 103, 122, 130 | 약: 감성 / 중: 기본 / 강: 하이라이트·이벤트 |
| 오버클럭 on/off | Tgl_Overclock | 015~023, 129, 134 | 클러치 플레이, 후원 폭주, 이벤트 |
| 눈 반짝 on/off | Tgl_EyeStar | 055 | 오프닝, 감사 인사, 신규 구독 |
| UI 패널 on/off | Tgl_UI | 010, 012 | 잡담 기본 on, 게임 중 off |
| 모바일폼 on/off | Tgl_Mobile | 013, 037 (헤드셋 off) | 모바일 방송, 세로 쇼츠 |
| 게임폼 on/off | Tgl_Game | 014, 038, 086 | 게임 방송 |
| glitch on/off | Tgl_Glitch | 008, 009, 061 | 렉/끊김, 개그 연출, 방송 사고 |
| 배터리 부족 on/off | Tgl_LowBattery | 011 (010 off), Glow 20% | 방송 종료 전, 피곤 연출 |
| 드론 on/off | Tgl_Drone | 131~133 | 풀샷 on, 클로즈업 off |
| 정령 링 on/off | Tgl_Ring | 126~128 | 기본 on, 게임 화면 가림 시 off |
| 얼굴 회로점 | Tgl_FaceMark | 075 | 기본 on |
| 이모트 4종 | Tgl_Emote_* | 003~006 | 리액션 |

## 2. 추천 표정 단축키 매핑
| 키 | 표정/동작 | 비고 |
|---|---|---|
| F1 | 기본 | 모든 표정 리셋 |
| F2 | 미소 | |
| F3 | 활짝 웃음 | |
| F4 | 당황 | 땀 이모트 포함 |
| F5 | 화남 | |
| F6 | 울먹 | |
| F7 | glitch | 3초 후 자동 해제 권장 |
| F8 | 오버클럭 | 토글 유지 |
| F9 | 놀람 | |
| F10 | 삐짐 | 후드 연동 옵션 |
| F11 | 장난기 | |
| F12 | 방송용 반짝임 | |
| Shift+F1 | 어이없음 | |
| Shift+F2 | 슬픔 | |
| Shift+F3 | 오버클럭 폭주 표정(표정만) | |
| Ctrl+1 | 헤드셋 토글 | |
| Ctrl+2 | 후드 토글 | |
| Ctrl+3 | 전기광 약→중→강 순환 | |
| Ctrl+4 | UI 패널 토글 | |
| Ctrl+5 | 모바일폼 | |
| Ctrl+6 | 게임폼 | |
| Ctrl+7 | 배터리 부족 | |
| Ctrl+8 | 드론 토글 | |
| Ctrl+9 | 정령 링 토글 | |
| Ctrl+0 | 전체 토글 리셋(기본 방송폼) | |

## 3. 방송 상황별 추천 토글 세트
| 세트 | 켜기 | 끄기 | 전기광 | 주 표정 키 |
|---|---|---|---|---|
| 잡담 방송 | 헤드셋, UI 패널, 드론, 링, 회로점 | 게임폼, OC | 중 | F1 F2 F3 F4 F11 |
| 게임 방송 | 게임폼(바이저·HUD·LED), 헤드셋, 드론 | UI 패널, 링(화면 가림 시) | 중→강 | F3 F4 F5 F7 F8 |
| 감성 방송 | 후드, 링 | 헤드셋, UI, 드론 | 약 | F2 F6 Shift+F2 |
| 쇼츠용 | 모바일폼, 드론, 눈 반짝 | UI 패널 | 강 | F3 F7 F8 F12 |
| 노래 방송 | 링, 눈 반짝(후렴) | 헤드셋(마이크 가림 방지), UI | 중 | F2 F12 |
| 방송 종료 | 배터리 부족, 후드 | UI 패널, OC | 약 | Shift+F2 → F2 |
| 이벤트/기념 | OC, 눈 반짝, 이모트 하트 | — | 강 | F8 F12 F3 |

## 4. PSD 레이어 매핑 (PHASE 7 최종, `layer_manifest_final.csv` 기준)
| 토글 | 파라미터 | 실제 레이어 |
|---|---|---|
| 헤드셋 on/off | Tgl_Headset | Headset_Band, Headset_Cup_R/L, Headset_Cup_Glow (+off 시 Hair_Headset_Press 표시) |
| 마이크 on/off | Tgl_Mic | Headset_Mic |
| 후드 on/off | Tgl_Hood | Hood_Up, Hair_Back_Hood ↔ Hood_Folded, Hair_Back_Base |
| 전기광 약/중/강 | Glow_Level | Ring_Spirit_Glow, Inner_Circuit_Glow, Core_Glow, Jacket_Hood_Rim_Glow, Sleeve_Cuff_Glow, Headset_Cup_Glow, Hair_Inner_Glow, Pip_Glow, Cable_Electric_Ribbon (불투명도) |
| 오버클럭 | Tgl_Overclock | OC_Ring_Outer, Drone_Trail_OC, OC_Warning_Panel, OC_Spark_Front, OC_Hair_Spark, OC_Eye_Ring_R/L, OC_Core_Burst, OC_Body_Rimlight |
| 눈 반짝 | Tgl_EyeStar | Eye_Star_Sparkle, FX_Sparkle_Front |
| UI 패널 | Tgl_UI | UI_Panel_L_Battery, UI_Panel_R_Signal |
| 배터리 부족 | Tgl_LowBattery | UI_Panel_L_Battery_Low, UI_Signal_Low, LowBattery_Dim |
| 모바일폼 | Tgl_Mobile | UI_Mobile_Frame, Earpiece_Mobile (+헤드셋 off) |
| 게임폼 | Tgl_Game | Visor_Game, UI_Game_HUD |
| glitch | Tgl_Glitch | FX_Glitch_Overlay, FX_Glitch_Block_1/2 |
| Pip / 링 | Tgl_Drone / Tgl_Ring | Drone_*, Pip_* / Ring_Spirit_* |
| 장갑 | Tgl_Glove | Hand_R_Glove, Hand_L_Glove |
| 얼굴 회로점 | Tgl_FaceMark | Face_Mark_Circuit |
| 이모트 | Tgl_Emote | FX_Emote_Heart / Sweat / Anger |
