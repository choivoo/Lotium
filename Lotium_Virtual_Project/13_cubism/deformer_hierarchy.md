# Deformer Hierarchy — Lotium

`DFM_*` = 워프/회전 디포머, 대문자 폴더 = 파츠(Part) 그룹. 괄호는 하위 ArtMesh 수.

```
└─ ROOT  (149 meshes)
   ├─ OVERCLOCK_ROOT  (4 meshes)
   ├─ BODY_ROOT  (127 meshes)
   │  └─ DFM_BODY_XY  (127 meshes)
   │     ├─ DFM_BODY_Z  (126 meshes)
   │     │  ├─ DFM_NECK  (80 meshes)
   │     │  │  └─ HEAD_ROOT  (77 meshes)
   │     │  │     ├─ DFM_HEAD_XY  (69 meshes)
   │     │  │     │  └─ DFM_HEAD_Z  (69 meshes)
   │     │  │     │     ├─ FACE  (44 meshes)
   │     │  │     │     │  ├─ EYES  (24 meshes)
   │     │  │     │     │  │  ├─ DFM_EYE_L  (10 meshes)
   │     │  │     │     │  │  │  └─ DFM_EYEBALL_L  (3 meshes)
   │     │  │     │     │  │  ├─ DFM_EYE_R  (10 meshes)
   │     │  │     │     │  │  │  └─ DFM_EYEBALL_R  (3 meshes)
   │     │  │     │     │  │  └─ DFM_EYES  (4 meshes)
   │     │  │     │     │  ├─ MOUTH  (10 meshes)
   │     │  │     │     │  │  └─ DFM_MOUTH  (10 meshes)
   │     │  │     │     │  ├─ BROWS  (2 meshes)
   │     │  │     │     │  │  ├─ DFM_BROW_L  (1 meshes)
   │     │  │     │     │  │  └─ DFM_BROW_R  (1 meshes)
   │     │  │     │     │  └─ DFM_FACE  (8 meshes)
   │     │  │     │     ├─ HEAD_ACCESSORIES  (8 meshes)
   │     │  │     │     │  └─ DFM_MIC  (1 meshes)
   │     │  │     │     ├─ FRONT_HAIR  (9 meshes)
   │     │  │     │     │  ├─ DFM_HAIR_FRONT  (5 meshes)
   │     │  │     │     │  ├─ DFM_HAIR_AHOGE  (1 meshes)
   │     │  │     │     │  ├─ DFM_HAIR_FRONT_C  (1 meshes)
   │     │  │     │     │  ├─ DFM_HAIR_FRONT_L  (1 meshes)
   │     │  │     │     │  └─ DFM_HAIR_FRONT_R  (1 meshes)
   │     │  │     │     ├─ SIDE_HAIR  (5 meshes)
   │     │  │     │     │  ├─ DFM_HAIR_SIDE_L  (2 meshes)
   │     │  │     │     │  ├─ DFM_HAIR_SIDE_R  (2 meshes)
   │     │  │     │     │  └─ DFM_HAIR_SIDE_LR  (1 meshes)
   │     │  │     │     └─ BACK_HAIR  (3 meshes)
   │     │  │     │        └─ DFM_HAIR_BACK  (3 meshes)
   │     │  │     └─ HEAD_FX  (8 meshes)
   │     │  ├─ TORSO  (7 meshes)
   │     │  │  └─ DFM_BREATH  (6 meshes)
   │     │  ├─ ARM_L  (8 meshes)
   │     │  │  └─ DFM_ARM_L  (8 meshes)
   │     │  │     └─ DFM_SLEEVE_L  (3 meshes)
   │     │  ├─ ARM_R  (8 meshes)
   │     │  │  └─ DFM_ARM_R  (8 meshes)
   │     │  │     └─ DFM_SLEEVE_R  (3 meshes)
   │     │  ├─ CLOTHES  (11 meshes)
   │     │  │  ├─ DFM_DRAWSTRING  (2 meshes)
   │     │  │  ├─ DFM_JACKET  (7 meshes)
   │     │  │  └─ DFM_HEM  (2 meshes)
   │     │  ├─ CABLE_ROOT  (5 meshes)
   │     │  │  └─ DFM_CABLE_1  (5 meshes)
   │     │  │     └─ DFM_CABLE_2  (3 meshes)
   │     │  │        └─ DFM_CABLE_3  (1 meshes)
   │     │  └─ LOWER_BODY  (7 meshes)
   │     └─ FX  (1 meshes)
   ├─ UI_ROOT  (6 meshes)
   │  └─ DFM_UI_FLOAT  (6 meshes)
   ├─ PIP_ROOT  (6 meshes)
   │  └─ DFM_PIP_FLOAT  (6 meshes)
   │     └─ DFM_PIP_ANTENNA  (1 meshes)
   └─ SPIRIT_RING_ROOT  (6 meshes)
      └─ DFM_RING_FLOAT  (6 meshes)
         └─ DFM_RING_ROT  (6 meshes)
```

## 디포머 종류·설정
| 디포머 | 종류 | 분할(워프) | 연결 파라미터 | 비고 |
|---|---|---|---|---|
| DFM_BODY_XY | 워프 | 5×5 | BodyAngleX, BodyAngleY | 몸 전체, 머리 이동량의 30~45% |
| DFM_BODY_Z | 회전 | – | BodyAngleZ | 피벗 = 허리 (1520, 2100) |
| DFM_BREATH | 워프 | 3×3 | Breath | 흉부 1.2% 확대 + 어깨 -6px |
| DFM_NECK | 워프 | 3×3 | AngleX/Y (10%) | 목 비틀림 완충 |
| HEAD_ROOT/DFM_HEAD_XY | 워프 | 6×6 | AngleX, AngleY | 얼굴 전체 pseudo-3D |
| DFM_HEAD_Z | 회전 | – | AngleZ | 피벗 = 턱 아래 (1520, 800) |
| DFM_FACE | 워프 | 5×5 | AngleX, AngleY | 얼굴 윤곽·귀·코 |
| DFM_EYE_L/R | 워프 | 3×3 | EyeL/ROpen, EyeL/RSmile | 눈꺼풀 닫기 |
| DFM_EYEBALL_L/R | 워프 | 2×2 | EyeBallX/Y, EyeBallForm | 흰자로 클리핑 |
| DFM_BROW_L/R | 워프 | 3×2 | BrowY/Angle/Form | |
| DFM_MOUTH | 워프 | 4×3 | MouthOpenY, MouthForm, MouthShape | |
| DFM_HAIR_FRONT_L/C/R, _AHOGE | 워프 | 3×4 | HairFront, Ahoge | 뿌리 고정 |
| DFM_HAIR_SIDE_L/R | 워프 | 3×5 | HairSide | |
| DFM_HAIR_BACK | 워프 | 4×4 | HairBack | |
| DFM_MIC | 회전 | – | MicSwing | 피벗 = 이어컵 |
| ARM_R/L/DFM_ARM_* | 회전 | – | ArmRA/ArmLA | 피벗 = 어깨 (1215,990)/(1850,990) |
| DFM_SLEEVE_* | 워프 | 3×3 | SleeveR/L | |
| DFM_HEM / DFM_DRAWSTRING | 워프 | 3×4 | Hem / Drawstring | |
| CABLE_ROOT/DFM_CABLE_1→2→3 | 회전 체인 | – | CableSwingX/Y | 피벗 = 포트 → 중간 → 플러그 |
| PIP_ROOT/DFM_PIP_FLOAT | 워프 | 2×2 | PipX, PipY | |
| SPIRIT_RING_ROOT/DFM_RING_* | 워프+회전 | 3×3 | RingFloat, RingRotate | 머리 이동을 50%만 따라감(물리) |
| UI_ROOT/DFM_UI_FLOAT | 워프 | 2×2 | (Idle 모션) | |
| OVERCLOCK_ROOT | 파츠 | – | Overclock | 불투명도만 |
