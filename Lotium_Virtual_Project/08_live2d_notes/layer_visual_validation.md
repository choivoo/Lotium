# Layer Visual Validation — FINAL (v2)

기준: 승인된 `LTM_FULLBODY_MASTER_v001` / `LTM_FACE_MASTER_v001` 실제 이미지와 대조(r1 PRELIMINARY 대체).

## 집계
- 기존 134: KEEP 106 / MODIFY 16 / REMOVE 12
- ADD(신규): 30
- **최종 유효 레이어: 149** (120~150 범위, 숫자 맞추기용 레이어 없음 — 전부 실제 픽셀 파츠, 빈/중복 0)

## 기존 레이어 판정
| No | Layer | 판정 | 비고 |
|---|---|---|---|
| 001 | Base_Guide | REMOVE | 가이드는 출력 파츠 아님 |
| 002 | Color_Guide | REMOVE | COLOR_MASTER로 대체 |
| 003 | FX_Emote_Heart | KEEP |  |
| 004 | FX_Emote_Question | REMOVE | 150 한도 내 우선순위 낮음 |
| 005 | FX_Emote_Sweat | KEEP |  |
| 006 | FX_Emote_Anger | KEEP |  |
| 007 | FX_Sparkle_Front | KEEP |  |
| 008 | FX_Glitch_Overlay | KEEP |  |
| 009 | FX_Glitch_Block | MODIFY | → FX_Glitch_Block_1/2 |
| 010 | UI_Panel_L_Battery | KEEP |  |
| 011 | UI_Panel_L_Battery_Low | KEEP |  |
| 012 | UI_Panel_R_Signal | KEEP |  |
| 013 | UI_Mobile_Frame | KEEP |  |
| 014 | UI_Game_HUD | KEEP |  |
| 015 | OC_Warning_Panel | KEEP |  |
| 016 | OC_Spark_Front | KEEP |  |
| 017 | OC_Hair_Lift | REMOVE | Design Lock: 헤어스타일 변경 금지 |
| 018 | OC_Hair_Spark | KEEP |  |
| 019 | OC_Eye_Ring_L | KEEP |  |
| 020 | OC_Eye_Ring_R | KEEP |  |
| 021 | OC_Core_Burst | KEEP |  |
| 022 | OC_Body_Rimlight | KEEP |  |
| 023 | OC_Cable_Float | REMOVE | 케이블 물리 파라미터로 대체 |
| 024 | Hair_Front_Ahoge | KEEP |  |
| 025 | Hair_Front_L | KEEP |  |
| 026 | Hair_Front_C | KEEP |  |
| 027 | Hair_Front_R | KEEP |  |
| 028 | Hair_Front_Center_Strand | KEEP |  |
| 029 | Hair_Front_Highlight | REMOVE | 하이라이트가 헤어 파츠에 베이크됨 |
| 030 | Hair_Temple_L | KEEP |  |
| 031 | Hair_Temple_R | KEEP |  |
| 032 | Headset_Band | KEEP |  |
| 033 | Headset_Cup_L | KEEP |  |
| 034 | Headset_Cup_R | KEEP |  |
| 035 | Headset_Cup_Glow | KEEP |  |
| 036 | Headset_Mic | KEEP |  |
| 037 | Earpiece_Mobile | KEEP |  |
| 038 | Visor_Game | KEEP |  |
| 039 | Brow_L | KEEP |  |
| 040 | Brow_R | KEEP |  |
| 041 | Eye_L_Lash_Upper | KEEP |  |
| 042 | Eye_L_Line_Lower | KEEP |  |
| 043 | Eye_L_Highlight | KEEP |  |
| 044 | Eye_L_Pupil | KEEP |  |
| 045 | Eye_L_Iris | KEEP |  |
| 046 | Eye_L_White | KEEP |  |
| 047 | Eye_L_Closed_Smile | KEEP |  |
| 048 | Eye_R_Lash_Upper | KEEP |  |
| 049 | Eye_R_Line_Lower | KEEP |  |
| 050 | Eye_R_Highlight | KEEP |  |
| 051 | Eye_R_Pupil | KEEP |  |
| 052 | Eye_R_Iris | KEEP |  |
| 053 | Eye_R_White | KEEP |  |
| 054 | Eye_R_Closed_Smile | KEEP |  |
| 055 | Eye_Star_Sparkle | KEEP |  |
| 056 | Eye_Flat_Deadpan | KEEP |  |
| 057 | Eye_Swirl_Dizzy | REMOVE | 14표정 외 |
| 058 | Eye_Tear_L | MODIFY | → Eye_Tears_Pool |
| 059 | Eye_Tear_R | MODIFY | → Eye_Tears_Pool |
| 060 | Tear_Stream | KEEP |  |
| 061 | Eye_Glitch_Pixel | REMOVE | FX_Glitch_Overlay로 통합 |
| 062 | Mouth_Line_Upper | KEEP |  |
| 063 | Mouth_Line_Lower | KEEP |  |
| 064 | Mouth_Teeth_Upper | KEEP |  |
| 065 | Mouth_Tongue | KEEP |  |
| 066 | Mouth_Inside | KEEP |  |
| 067 | Mouth_Pout | KEEP |  |
| 068 | Mouth_Cat_Grin | MODIFY | → Mouth_Grin_Mischief |
| 069 | Mouth_Wavy | KEEP |  |
| 070 | Face_Blush | KEEP |  |
| 071 | Face_Blush_Strong | KEEP |  |
| 072 | Face_Shadow_Dark | KEEP |  |
| 073 | Face_Sweat | REMOVE | FX_Emote_Sweat로 통합 |
| 074 | Face_Cheek_Puff | REMOVE | 볼 변형 파라미터로 대체 |
| 075 | Face_Mark_Circuit | KEEP |  |
| 076 | Nose | KEEP |  |
| 077 | Face_Shadow_Hair | KEEP |  |
| 078 | Face_Base | KEEP |  |
| 079 | Hair_Side_L_Front | MODIFY | → Hair_Side_L_Upper |
| 080 | Hair_Side_L_Back | MODIFY | → Hair_Side_L_Lower |
| 081 | Hair_Side_R_Front | MODIFY | → Hair_Side_R_Upper |
| 082 | Hair_Side_R_Back | MODIFY | → Hair_Side_R_Lower |
| 083 | Ear_L | KEEP |  |
| 084 | Ear_R | KEEP |  |
| 085 | Hand_R | KEEP |  |
| 086 | Hand_R_Glove_LED | REMOVE | 마스터 장갑에 LED 없음 |
| 087 | Sleeve_R_Cuff | KEEP |  |
| 088 | Sleeve_R_Inner | KEEP |  |
| 089 | Arm_R_Forearm | KEEP |  |
| 090 | Arm_R_Upper | KEEP |  |
| 091 | Core_Glow | KEEP |  |
| 092 | Core_Gauge_Ring | MODIFY | → Core_Glow |
| 093 | Core_Face | KEEP |  |
| 094 | Core_Case | KEEP |  |
| 095 | Drawstring_L | KEEP |  |
| 096 | Drawstring_R | KEEP |  |
| 097 | Jacket_Zipper_Glow | MODIFY | → Jacket_Hood_Rim_Glow |
| 098 | Jacket_Front_L | KEEP |  |
| 099 | Jacket_Front_R | KEEP |  |
| 100 | Jacket_Collar | KEEP |  |
| 101 | Jacket_Strap | MODIFY | → Pants_Strap_R/L |
| 102 | Jacket_Hem_Front | MODIFY | → Jacket_Hem_R/L |
| 103 | Inner_Circuit_Glow | KEEP |  |
| 104 | Inner_Body | KEEP |  |
| 105 | Neck_Choker | REMOVE | 마스터에 초커 없음(하이넥 이너) |
| 106 | Neck | KEEP |  |
| 107 | Pants_L | KEEP |  |
| 108 | Pants_R | KEEP |  |
| 109 | Leg_Thigh_Base | MODIFY | → Pants_R/L (restored) |
| 110 | Shoe_L | KEEP |  |
| 111 | Shoe_R | KEEP |  |
| 112 | Hand_L | KEEP |  |
| 113 | Sleeve_L_Cuff | KEEP |  |
| 114 | Arm_L_Forearm | KEEP |  |
| 115 | Arm_L_Upper | KEEP |  |
| 116 | Hood_Folded | KEEP |  |
| 117 | Hood_Up | KEEP |  |
| 118 | Jacket_Back_Hem | MODIFY | → Jacket_Back_Lining |
| 119 | Cable_Tail_Seg1 | KEEP |  |
| 120 | Cable_Tail_Seg2 | KEEP |  |
| 121 | Cable_Tail_Plug | KEEP |  |
| 122 | Cable_Electric_Ribbon | KEEP |  |
| 123 | Hair_Back_Upper | MODIFY | → Hair_Back_Base |
| 124 | Hair_Back_Lower | KEEP |  |
| 125 | Hair_Back_Hood | KEEP |  |
| 126 | Ring_Spirit_Seg1 | KEEP |  |
| 127 | Ring_Spirit_Seg2 | KEEP |  |
| 128 | Ring_Spirit_Seg3 | KEEP |  |
| 129 | OC_Ring_Outer | KEEP |  |
| 130 | FX_Aura_Glow_Back | MODIFY | → Ring_Spirit_Glow |
| 131 | Drone_Body | KEEP |  |
| 132 | Drone_Antenna | KEEP |  |
| 133 | Drone_Eye | KEEP |  |
| 134 | Drone_Trail_OC | KEEP |  |

## ADD
- Arm_L_Under
- Arm_R_Under
- Cable_Port
- Eye_L_Closed_Line
- Eye_L_Lid_Skin
- Eye_R_Closed_Line
- Eye_R_Lid_Skin
- FX_Glitch_Block_2
- Hair_Headset_Press
- Hair_Inner_Glow
- Hand_L_Glove
- Hand_R_Glove
- Jacket_Hem_L
- Jacket_Side_Under_Arm_L
- Jacket_Side_Under_Arm_R
- LowBattery_Dim
- Mouth_Closed_Smile
- Mouth_Teeth_Lower
- Neck_Back
- Pants_Strap_L
- Pants_Waist_Restore
- Pip_Glow
- Pip_Hover_Ring
- Ring_Spirit_Seg4
- Sleeve_Cuff_Glow
- Sleeve_L_Inner
- Sleeve_L_Strap
- Sleeve_R_Strap
- Torso_Restore
- UI_Signal_Low
