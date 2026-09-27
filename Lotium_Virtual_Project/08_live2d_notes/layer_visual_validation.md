# Layer Visual Validation (134 → 최종)

**상태: PRELIMINARY (스펙 기준)** — Fullbody Master 이미지가 없어 실제 이미지 대조는 미완료. 이미지 확보 후 이 문서를 v2로 갱신.

판정: KEEP 그대로 / MODIFY 수정 / REMOVE 제거 / ADD 신규

## 기존 레이어
| No | Layer | 판정 | 비고 |
|---|---|---|---|
| 001 | Base_Guide | KEEP |  |
| 002 | Color_Guide | REMOVE | COLOR_MASTER 이미지로 대체, PSD 가이드 불필요 |
| 003 | FX_Emote_Heart | KEEP |  |
| 004 | FX_Emote_Question | KEEP |  |
| 005 | FX_Emote_Sweat | KEEP |  |
| 006 | FX_Emote_Anger | KEEP |  |
| 007 | FX_Sparkle_Front | KEEP |  |
| 008 | FX_Glitch_Overlay | KEEP |  |
| 009 | FX_Glitch_Block | MODIFY | 픽셀 블록은 3조각 개별 레이어로 분할 검토(깜빡임 개별 제어) |
| 010 | UI_Panel_L_Battery | KEEP |  |
| 011 | UI_Panel_L_Battery_Low | KEEP |  |
| 012 | UI_Panel_R_Signal | KEEP |  |
| 013 | UI_Mobile_Frame | KEEP |  |
| 014 | UI_Game_HUD | KEEP |  |
| 015 | OC_Warning_Panel | KEEP |  |
| 016 | OC_Spark_Front | KEEP |  |
| 017 | OC_Hair_Lift | MODIFY | OC 머리는 대체 아닌 끝 들림 변형+스파크 — 헤어스타일 자체 변경 금지(Design Lock) |
| 018 | OC_Hair_Spark | KEEP |  |
| 019 | OC_Eye_Ring_L | KEEP |  |
| 020 | OC_Eye_Ring_R | KEEP |  |
| 021 | OC_Core_Burst | KEEP |  |
| 022 | OC_Body_Rimlight | MODIFY | 림라이트는 가는 시안 선만. 전신 색 오라 외곽선은 로토무 연상 → 두께 제한 |
| 023 | OC_Cable_Float | REMOVE | 케이블 Seg 변형 파라미터로 부유 구현 → 대체 레이어 불필요 |
| 024 | Hair_Front_Ahoge | KEEP |  |
| 025 | Hair_Front_L | KEEP |  |
| 026 | Hair_Front_C | KEEP |  |
| 027 | Hair_Front_R | KEEP |  |
| 028 | Hair_Front_Center_Strand | KEEP |  |
| 029 | Hair_Front_Highlight | KEEP |  |
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
| 057 | Eye_Swirl_Dizzy | REMOVE | 14표정 목록 외 → 제거(당황은 069+073) |
| 058 | Eye_Tear_L | KEEP |  |
| 059 | Eye_Tear_R | KEEP |  |
| 060 | Tear_Stream | KEEP |  |
| 061 | Eye_Glitch_Pixel | KEEP |  |
| 062 | Mouth_Line_Upper | KEEP |  |
| 063 | Mouth_Line_Lower | KEEP |  |
| 064 | Mouth_Teeth_Upper | KEEP |  |
| 065 | Mouth_Tongue | KEEP |  |
| 066 | Mouth_Inside | KEEP |  |
| 067 | Mouth_Pout | KEEP |  |
| 068 | Mouth_Cat_Grin | MODIFY | Mouth_Cat_Grin → Mouth_Grin_Mischief (ω 고양이입 오해 방지) |
| 069 | Mouth_Wavy | KEEP |  |
| 070 | Face_Blush | KEEP |  |
| 071 | Face_Blush_Strong | KEEP |  |
| 072 | Face_Shadow_Dark | KEEP |  |
| 073 | Face_Sweat | KEEP |  |
| 074 | Face_Cheek_Puff | KEEP |  |
| 075 | Face_Mark_Circuit | KEEP |  |
| 076 | Nose | KEEP |  |
| 077 | Face_Shadow_Hair | KEEP |  |
| 078 | Face_Base | KEEP |  |
| 079 | Hair_Side_L_Front | KEEP |  |
| 080 | Hair_Side_L_Back | KEEP |  |
| 081 | Hair_Side_R_Front | KEEP |  |
| 082 | Hair_Side_R_Back | KEEP |  |
| 083 | Ear_L | KEEP |  |
| 084 | Ear_R | KEEP |  |
| 085 | Hand_R | KEEP |  |
| 086 | Hand_R_Glove_LED | KEEP |  |
| 087 | Sleeve_R_Cuff | KEEP |  |
| 088 | Sleeve_R_Inner | KEEP |  |
| 089 | Arm_R_Forearm | KEEP |  |
| 090 | Arm_R_Upper | KEEP |  |
| 091 | Core_Glow | KEEP |  |
| 092 | Core_Gauge_Ring | KEEP |  |
| 093 | Core_Face | KEEP |  |
| 094 | Core_Case | KEEP |  |
| 095 | Drawstring_L | KEEP |  |
| 096 | Drawstring_R | KEEP |  |
| 097 | Jacket_Zipper_Glow | KEEP |  |
| 098 | Jacket_Front_L | KEEP |  |
| 099 | Jacket_Front_R | KEEP |  |
| 100 | Jacket_Collar | KEEP |  |
| 101 | Jacket_Strap | KEEP |  |
| 102 | Jacket_Hem_Front | KEEP |  |
| 103 | Inner_Circuit_Glow | KEEP |  |
| 104 | Inner_Body | KEEP |  |
| 105 | Neck_Choker | KEEP |  |
| 106 | Neck | KEEP |  |
| 107 | Pants_L | KEEP |  |
| 108 | Pants_R | KEEP |  |
| 109 | Leg_Thigh_Base | KEEP |  |
| 110 | Shoe_L | KEEP |  |
| 111 | Shoe_R | KEEP |  |
| 112 | Hand_L | KEEP |  |
| 113 | Sleeve_L_Cuff | KEEP |  |
| 114 | Arm_L_Forearm | KEEP |  |
| 115 | Arm_L_Upper | KEEP |  |
| 116 | Hood_Folded | KEEP |  |
| 117 | Hood_Up | MODIFY | Hood_Up은 03_HAIR_FRONT 위 그룹으로 이동(Z-order) |
| 118 | Jacket_Back_Hem | KEEP |  |
| 119 | Cable_Tail_Seg1 | KEEP |  |
| 120 | Cable_Tail_Seg2 | KEEP |  |
| 121 | Cable_Tail_Plug | KEEP |  |
| 122 | Cable_Electric_Ribbon | KEEP |  |
| 123 | Hair_Back_Upper | KEEP |  |
| 124 | Hair_Back_Lower | KEEP |  |
| 125 | Hair_Back_Hood | KEEP |  |
| 126 | Ring_Spirit_Seg1 | KEEP |  |
| 127 | Ring_Spirit_Seg2 | KEEP |  |
| 128 | Ring_Spirit_Seg3 | KEEP |  |
| 129 | OC_Ring_Outer | KEEP |  |
| 130 | FX_Aura_Glow_Back | MODIFY | FX_Aura_Glow_Back → FX_Back_Glow_Small: 코어·링 주변 국소 글로우만. 전신 오라 금지 |
| 131 | Drone_Body | KEEP |  |
| 132 | Drone_Antenna | KEEP |  |
| 133 | Drone_Eye | KEEP |  |
| 134 | Drone_Trail_OC | KEEP |  |

## ADD
| 임시 No | Layer | 폴더 | 이유 |
|---|---|---|---|
| A01 | Eye_L_Lid_Skin | 05_FACE/Eye_L | 눈 감을 때 덮는 눈꺼풀 피부(hidden 복원) |
| A02 | Eye_R_Lid_Skin | 05_FACE/Eye_R | 눈 감을 때 덮는 눈꺼풀 피부 |
| A03 | Eye_L_Closed_Line | 05_FACE/Eye_L | 기본 감은눈 라인(눈 깜빡임) |
| A04 | Eye_R_Closed_Line | 05_FACE/Eye_R | 기본 감은눈 라인 |
| A05 | Mouth_Teeth_Lower | 05_FACE/Mouth | 아랫니(크게 벌린 입) |
| A06 | Face_Base_Side_L | 05_FACE/Face_Base | 머리 회전용 얼굴 측면 윤곽 좌(hidden) |
| A07 | Face_Base_Side_R | 05_FACE/Face_Base | 얼굴 측면 윤곽 우 |
| A08 | Hair_Headset_Press | 03_HAIR_FRONT | 헤드셋 착용 시 눌린 머리 경계(헤드셋 off 대응) |
| A09 | Neck_Back | 10_BODY | 목 뒤(칼라 뒤 복원) |
| A10 | Torso_Under_Arm_L | 10_BODY | 팔 뒤 몸통 좌(hidden) |
| A11 | Torso_Under_Arm_R | 10_BODY | 팔 뒤 몸통 우(hidden) |
| A12 | Wrist_R | 08_ARM_R_FRONT | 소매 안 손목(hidden) |
| A13 | Wrist_L | 11_ARM_L | 소매 안 손목(hidden) |
| A14 | Sleeve_L_Inner | 11_ARM_L | 왼 소매 안쪽면(좌우 대칭 누락 보완) |
| A15 | Jacket_Panel_Orange_L | 09_BODY_FRONT | 오렌지 옆 패널 좌(색 교체·그림자 분리) |
| A16 | Jacket_Panel_Orange_R | 09_BODY_FRONT | 오렌지 옆 패널 우 |
| A17 | Cable_Port | 12_BACK | 허리 뒤 포트 단독(케이블 물리 기준점) |
| A18 | Pip_Glow | 15_DRONE | Pip LED/바디 글로우(Add) |

## 집계
- KEEP 125 / MODIFY 6 / REMOVE 3 / ADD 18
- 예상 최종 레이어: 149개 (120~150 범위 내)
- 이미지 대조 후 추가 REMOVE/ADD 가능.
