#!/usr/bin/env python3
"""Generate the Lotium Cubism rig specification + runtime JSON (physics3/exp3/cdi3/model3)
from 08_live2d_notes/parts_assembly_manifest.json (PSD v003)."""
import csv
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "13_cubism"
EXP = OUT / "LTM_VTubeStudio_Export"
(EXP / "expressions").mkdir(parents=True, exist_ok=True)
M = json.loads((ROOT / "08_live2d_notes/parts_assembly_manifest.json").read_text())
L = M["layers"]
base = lambda l: l["name"].split("_", 1)[1]
S = 1.0  # manifest coords are canvas px (3072x4608)

# ------------------------------------------------------------------ parameters
P = []  # id, name(ko), min, default, max, group, note
def prm(i, n, a, d, b, g, note=""):
    P.append(dict(id=i, name=n, min=a, default=d, max=b, group=g, note=note))
for i, n in [("ParamAngleX", "고개 좌우"), ("ParamAngleY", "고개 상하"), ("ParamAngleZ", "고개 기울기")]:
    prm(i, n, -30, 0, 30, "Face")
for i, n in [("ParamBodyAngleX", "몸 좌우"), ("ParamBodyAngleY", "몸 앞뒤"), ("ParamBodyAngleZ", "몸 기울기")]:
    prm(i, n, -10, 0, 10, "Body")
prm("ParamEyeLOpen", "왼눈 뜨기", 0, 1, 1, "Eyes"); prm("ParamEyeLSmile", "왼눈 웃음", 0, 0, 1, "Eyes")
prm("ParamEyeROpen", "오른눈 뜨기", 0, 1, 1, "Eyes"); prm("ParamEyeRSmile", "오른눈 웃음", 0, 0, 1, "Eyes")
prm("ParamEyeBallX", "눈동자 X", -1, 0, 1, "Eyes"); prm("ParamEyeBallY", "눈동자 Y", -1, 0, 1, "Eyes")
prm("ParamEyeBallForm", "동공 크기", -1, 0, 1, "Eyes", "놀람 시 축소")
for s in "LR":
    prm(f"ParamBrow{s}Y", f"{s} 눈썹 높이", -1, 0, 1, "Brows")
    prm(f"ParamBrow{s}Angle", f"{s} 눈썹 각도", -1, 0, 1, "Brows")
    prm(f"ParamBrow{s}Form", f"{s} 눈썹 모양", -1, 0, 1, "Brows")
prm("ParamMouthForm", "입 모양(-찡그림/+웃음)", -1, 0, 1, "Mouth"); prm("ParamMouthOpenY", "입 벌리기", 0, 0, 1, "Mouth")
prm("ParamMouthShape", "입 모음(A/I/U/E/O 보조)", -1, 0, 1, "Mouth", "-1=U/O 오므림, +1=I/E 옆으로")
prm("ParamCheek", "볼 홍조", 0, 0, 1, "Face")
prm("ParamBreath", "호흡", 0, 0, 1, "Body")
for i, n in [("ParamHairFront", "앞머리 흔들림"), ("ParamHairSide", "옆머리 흔들림"), ("ParamHairBack", "뒷머리 흔들림"),
             ("ParamAhoge", "아호게 흔들림"), ("ParamDrawstring", "후드끈 흔들림"), ("ParamHem", "밑단 흔들림"),
             ("ParamSleeveR", "오른 소매 흔들림"), ("ParamSleeveL", "왼 소매 흔들림"), ("ParamStrap", "스트랩 흔들림"),
             ("ParamCableSwingX", "케이블 X"), ("ParamCableSwingY", "케이블 Y"), ("ParamPipAntenna", "핍 안테나"),
             ("ParamRingFloat", "정령 링 부유"), ("ParamMicSwing", "마이크 흔들림")]:
    prm(i, n, -1, 0, 1, "Physics")
prm("ParamArmRA", "오른팔 각도", -1, 0, 1, "Body"); prm("ParamArmLA", "왼팔 각도", -1, 0, 1, "Body")
prm("ParamPipX", "핍 X", -1, 0, 1, "Accessory"); prm("ParamPipY", "핍 Y", -1, 0, 1, "Accessory")
prm("ParamRingRotate", "정령 링 회전", -1, 0, 1, "Accessory")
prm("ParamCoreGlow", "코어 발광", 0, 0.5, 1, "FX"); prm("ParamElectricFX", "전기광 강도(약·중·강)", 0, 0.5, 1, "FX")
prm("ParamGlitch", "글리치", 0, 0, 1, "FX"); prm("ParamOverclock", "오버클럭", 0, 0, 1, "FX")
for i, n, d in [("ParamHeadset", "헤드셋", 1), ("ParamMic", "마이크", 1), ("ParamHood", "후드", 0), ("ParamUI", "UI 패널", 1),
                ("ParamMobile", "모바일폼", 0), ("ParamGame", "게임폼", 0), ("ParamLowBattery", "배터리 부족", 0),
                ("ParamPip", "드론 핍", 1), ("ParamRing", "정령 링", 1), ("ParamGlove", "장갑", 1), ("ParamFaceMark", "얼굴 회로점", 1),
                ("ParamEyeStar", "눈 반짝", 0), ("ParamTears", "눈물", 0), ("ParamBlushStrong", "진한 홍조", 0),
                ("ParamShadowDark", "얼굴 그늘", 0), ("ParamDeadpan", "무표정 눈", 0),
                ("ParamEmoteHeart", "이모트 하트", 0), ("ParamEmoteSweat", "이모트 땀", 0), ("ParamEmoteAnger", "이모트 분노", 0)]:
    prm(i, n, 0, d, 1, "Toggle", "0/1 스위치 (파츠 불투명도 키폼 2개)")
PID = {p["id"] for p in P}

# ------------------------------------------------------------------ layer -> deformer/mesh/params
def classify(n, g):
    """returns deformer path, mesh preset, driving params, opacity rule"""
    head = g in ("02_BACK_HAIR", "05_FACE", "06_EYES", "07_BROWS", "08_MOUTH", "09_HEADSET", "10_FRONT_HAIR") or \
        n in ("Visor_Game", "Earpiece_Mobile", "Hood_Up", "OC_Hair_Spark", "OC_Eye_Ring_R", "OC_Eye_Ring_L",
              "FX_Glitch_Overlay", "FX_Glitch_Block_1", "FX_Glitch_Block_2", "FX_Sparkle_Front",
              "FX_Emote_Heart", "FX_Emote_Sweat", "FX_Emote_Anger")
    mesh, params, rule = "standard", [], ""
    if n.startswith("Ring_") or n == "OC_Ring_Outer":
        d = "ROOT/SPIRIT_RING_ROOT/DFM_RING_FLOAT/DFM_RING_ROT"; mesh = "simple"; params = ["ParamRingFloat", "ParamRingRotate"]
    elif n.startswith(("Drone_", "Pip_")):
        d = "ROOT/PIP_ROOT/DFM_PIP_FLOAT" + ("/DFM_PIP_ANTENNA" if n == "Drone_Antenna" else ""); mesh = "simple"; params = ["ParamPipX", "ParamPipY"] + (["ParamPipAntenna"] if n == "Drone_Antenna" else [])
    elif n.startswith("UI_"):
        d = "ROOT/UI_ROOT/DFM_UI_FLOAT"; mesh = "simple"
    elif n.startswith("Cable_"):
        d = "ROOT/BODY_ROOT/DFM_BODY_XY/DFM_BODY_Z/CABLE_ROOT/DFM_CABLE_1" + ("/DFM_CABLE_2" if n in ("Cable_Tail_Seg2", "Cable_Tail_Plug", "Cable_Electric_Ribbon") else "") + ("/DFM_CABLE_3" if n in ("Cable_Tail_Plug",) else "")
        mesh = "strip_dense"; params = ["ParamCableSwingX", "ParamCableSwingY"]
    elif n.startswith(("OC_", "FX_", "LowBattery")) and not head:
        d = "ROOT/OVERCLOCK_ROOT" if n.startswith("OC_") else "ROOT/BODY_ROOT/DFM_BODY_XY/FX"; mesh = "simple"
    elif head:
        hp = "ROOT/BODY_ROOT/DFM_BODY_XY/DFM_BODY_Z/DFM_NECK/HEAD_ROOT/DFM_HEAD_XY/DFM_HEAD_Z"
        if n.startswith(("Hair_Front", "Hair_Temple")) or n == "Hair_Inner_Glow":
            sub = "DFM_HAIR_AHOGE" if n == "Hair_Front_Ahoge" else ("DFM_HAIR_FRONT_" + n.split("_")[-1] if n.startswith("Hair_Front_") and n.split("_")[-1] in ("L", "C", "R") else "DFM_HAIR_FRONT")
            d = f"{hp}/FRONT_HAIR/{sub}"; mesh = "hair_strand"; params = ["ParamHairFront"] if "AHOGE" not in sub else ["ParamAhoge"]
        elif n.startswith("Hair_Side") or n == "Hair_Under_Headset":
            side = "R" if "_R_" in n else ("L" if "_L_" in n else "LR")
            d = f"{hp}/SIDE_HAIR/DFM_HAIR_SIDE_{side}"; mesh = "hair_strand"; params = ["ParamHairSide"]
        elif n.startswith("Hair_Back"):
            d = f"{hp}/BACK_HAIR/DFM_HAIR_BACK"; mesh = "hair_mass"; params = ["ParamHairBack"]
        elif n.startswith(("Eye_", "Tear", "OC_Eye")):
            side = "R" if "_R_" in n or n.endswith("_R") else ("L" if "_L_" in n or n.endswith("_L") else "LR")
            sub = f"DFM_EYE_{side}" if side != "LR" else "DFM_EYES"
            if any(k in n for k in ("Iris", "Pupil", "Highlight")):
                sub += "/DFM_EYEBALL_" + side
            d = f"{hp}/FACE/EYES/{sub}"; mesh = "eye_fine" if ("Lash" in n or "White" in n or "Lid" in n or "Line" in n) else "standard"
            params = [f"ParamEye{side}Open" if side != "LR" else "ParamEyeLOpen"] + (["ParamEyeBallX", "ParamEyeBallY"] if "EYEBALL" in sub else [])
        elif n.startswith("Brow_"):
            d = f"{hp}/FACE/BROWS/DFM_BROW_{n[-1]}"; mesh = "brow"; params = [f"ParamBrow{n[-1]}Y", f"ParamBrow{n[-1]}Angle", f"ParamBrow{n[-1]}Form"]
        elif n.startswith("Mouth_"):
            d = f"{hp}/FACE/MOUTH/DFM_MOUTH"; mesh = "mouth_fine"; params = ["ParamMouthOpenY", "ParamMouthForm"]
        elif n.startswith(("Headset_", "Earpiece", "Visor", "Hood_Up")):
            d = f"{hp}/HEAD_ACCESSORIES" + ("/DFM_MIC" if n == "Headset_Mic" else ""); mesh = "standard"
        elif n.startswith(("FX_", "OC_")):
            d = "ROOT/BODY_ROOT/DFM_BODY_XY/DFM_BODY_Z/DFM_NECK/HEAD_ROOT/HEAD_FX"; mesh = "simple"
        else:
            d = f"{hp}/FACE/DFM_FACE"; mesh = "face_fine" if n == "Face_Base" else ("standard" if not n.startswith("Ear") else "standard")
            params = ["ParamAngleX", "ParamAngleY"]
    else:
        bp = "ROOT/BODY_ROOT/DFM_BODY_XY/DFM_BODY_Z"
        if n.startswith(("Arm_R", "Sleeve_R", "Hand_R")):
            d = f"{bp}/ARM_R/DFM_ARM_R" + ("/DFM_SLEEVE_R" if n.startswith("Sleeve_R") else "")
            mesh = "limb"; params = ["ParamArmRA"] + (["ParamSleeveR"] if n.startswith("Sleeve_R") else [])
        elif n.startswith(("Arm_L", "Sleeve_L", "Hand_L")):
            d = f"{bp}/ARM_L/DFM_ARM_L" + ("/DFM_SLEEVE_L" if n.startswith("Sleeve_L") else "")
            mesh = "limb"; params = ["ParamArmLA"] + (["ParamSleeveL"] if n.startswith("Sleeve_L") else [])
        elif n.startswith(("Neck", "Hood_Folded")):
            d = f"{bp}/DFM_NECK"; mesh = "standard"
        elif n.startswith(("Pants", "Shoe", "Leg")):
            d = f"{bp}/LOWER_BODY"; mesh = "standard"
        elif n.startswith(("Jacket_Hem", "Drawstring")):
            d = f"{bp}/CLOTHES/DFM_" + ("HEM" if "Hem" in n else "DRAWSTRING"); mesh = "strip_dense"; params = ["ParamHem" if "Hem" in n else "ParamDrawstring"]
        elif n.startswith(("Jacket", "Inner", "Torso", "Core", "Pants_Waist")):
            d = f"{bp}/TORSO/DFM_BREATH" if n.startswith(("Inner", "Torso", "Core")) else f"{bp}/CLOTHES/DFM_JACKET"
            mesh = "standard"; params = ["ParamBreath"] + (["ParamCoreGlow"] if n.startswith("Core") else [])
        else:
            d = f"{bp}/TORSO"; mesh = "standard"
    return d, mesh, params

TOG = {  # layer prefix -> (param, value that SHOWS the layer)
    "Headset_": ("ParamHeadset", 1), "Headset_Mic": ("ParamMic", 1), "Hood_Up": ("ParamHood", 1), "Hair_Back_Hood": ("ParamHood", 1),
    "Hood_Folded": ("ParamHood", 0), "Hair_Back_Base": ("ParamHood", 0), "UI_Panel_L_Battery_Low": ("ParamLowBattery", 1),
    "UI_Signal_Low": ("ParamLowBattery", 1), "LowBattery_Dim": ("ParamLowBattery", 1), "UI_Panel_": ("ParamUI", 1),
    "UI_Mobile_Frame": ("ParamMobile", 1), "Earpiece_Mobile": ("ParamMobile", 1), "UI_Game_HUD": ("ParamGame", 1),
    "Visor_Game": ("ParamGame", 1), "Drone_Trail_OC": ("ParamOverclock", 1), "Drone_": ("ParamPip", 1), "Pip_": ("ParamPip", 1),
    "OC_": ("ParamOverclock", 1), "Ring_Spirit_": ("ParamRing", 1), "Hand_R_Glove": ("ParamGlove", 1), "Hand_L_Glove": ("ParamGlove", 1),
    "Face_Mark": ("ParamFaceMark", 1), "Eye_Star": ("ParamEyeStar", 1), "FX_Sparkle": ("ParamEyeStar", 1),
    "Eye_Tears": ("ParamTears", 1), "Tear_Stream": ("ParamTears", 1), "Face_Blush_Strong": ("ParamBlushStrong", 1),
    "Face_Shadow_Dark": ("ParamShadowDark", 1), "Eye_Flat_Deadpan": ("ParamDeadpan", 1), "FX_Glitch_": ("ParamGlitch", 1),
    "FX_Emote_Heart": ("ParamEmoteHeart", 1), "FX_Emote_Sweat": ("ParamEmoteSweat", 1), "FX_Emote_Anger": ("ParamEmoteAnger", 1),
    "Eye_R_Closed_Smile": ("ParamEyeRSmile", 1), "Eye_L_Closed_Smile": ("ParamEyeLSmile", 1),
    "Mouth_Pout": ("ParamMouthForm", "-1 & Open<0.1"), "Mouth_Wavy": ("ParamMouthShape", "-1 & Open 0.1–0.3"),
    "Mouth_Grin_Mischief": ("ParamMouthForm", "+1 & Open 0.2–0.5"), "Mouth_Closed_Smile": ("ParamMouthOpenY", "0 (Open<0.1)"),
}
def toggle_of(n):
    best = None
    for k, v in TOG.items():
        if n.startswith(k) and (best is None or len(k) > len(best[0])):
            best = (k, v)
    return best[1] if best else None

rows = []
for l in sorted(L, key=lambda l: l["z"]):
    n = base(l)
    d, mesh, params = classify(n, l["group"])
    t = toggle_of(n)
    if t:
        params = params + [t[0]]
    rows.append(dict(id=l["id"], layer=l["name"], artmesh=f"AM_{n}", group=l["group"], deformer=d, mesh_preset=mesh,
                     params=";".join(dict.fromkeys(params)), toggle=f"{t[0]}={t[1]}" if t else "",
                     blend="Additive" if l["blend"] == "add" else "Normal", visible_default=l["visible"],
                     physics=l["physics"], hidden_restored=l["hidden_restored"], x=l["x"], y=l["y"], w=l["w"], h=l["h"]))
bad = [r for r in rows for p in r["params"].split(";") if p and p not in PID]
assert not bad, bad[:3]

MESH = {
    "face_fine": "수동: 외곽 1줄(간격 24px) + 내부 격자 48px, 눈·코·입 주변 16px 보조 정점, 턱끝·볼 정점 추가",
    "eye_fine": "수동: 눈꺼풀 라인 따라 8–10정점, 상하 2열 (감기 변형용)",
    "mouth_fine": "수동: 입꼬리 좌우 + 윗/아랫입술선 각 6정점, 내부 2열",
    "brow": "자동(경계 여백 6, 간격 20) 후 길이방향 6정점",
    "hair_strand": "자동(경계 여백 8, 외곽 간격 40, 내부 간격 80) + 뿌리→끝 3~5단 세로 분할",
    "hair_mass": "자동(외곽 50, 내부 100)",
    "strip_dense": "자동 후 길이방향 6~8단 (굽힘용)",
    "limb": "자동(외곽 40, 내부 90) + 팔꿈치·손목 가로 루프",
    "standard": "자동(외곽 40, 내부 100)",
    "simple": "자동(외곽 60, 내부 200) 또는 사각 4정점",
}
with open(OUT / "artmesh_plan.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) + ["mesh_recipe"])
    w.writeheader()
    for r in rows:
        w.writerow(r | {"mesh_recipe": MESH[r["mesh_preset"]]})
with open(OUT / "parameters.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(P[0].keys()))
    w.writeheader(); w.writerows(P)

# deformer tree
tree = OrderedDict()
for r in rows:
    node = tree
    for part in r["deformer"].split("/"):
        node = node.setdefault(part, OrderedDict())
    node.setdefault("__layers__", []).append(r["artmesh"])
def dump(node, pre=""):
    out = []
    keys = [k for k in node if k != "__layers__"]
    for i, k in enumerate(keys):
        last = i == len(keys) - 1
        cnt = sum(1 for _ in walk(node[k]))
        out.append(f"{pre}{'└─' if last else '├─'} {k}  ({cnt} meshes)")
        out += dump(node[k], pre + ("   " if last else "│  "))
    return out
def walk(node):
    for k, v in node.items():
        if k == "__layers__":
            yield from v
        else:
            yield from walk(v)

# ------------------------------------------------------------------ physics3.json
def phys(name, inputs, outputs, n_vtx, length, mobility=0.95, delay=0.9, accel=1.5, radius=None):
    verts = [{"Position": {"X": 0, "Y": 0}, "Mobility": 1, "Delay": 1, "Acceleration": 1, "Radius": 0}]
    for i in range(1, n_vtx):
        verts.append({"Position": {"X": 0, "Y": round(length * i, 1)}, "Mobility": mobility, "Delay": delay,
                      "Acceleration": accel, "Radius": radius or length})
    return {"Id": name, "Input": [{"Source": {"Target": "Parameter", "Id": i}, "Weight": w, "Type": t, "Reflect": False} for i, w, t in inputs],
            "Output": [{"Destination": {"Target": "Parameter", "Id": o}, "VertexIndex": vi, "Scale": sc, "Weight": 100, "Type": "Angle", "Reflect": False} for o, vi, sc in outputs],
            "Vertices": verts,
            "Normalization": {"Position": {"Minimum": -10, "Default": 0, "Maximum": 10}, "Angle": {"Minimum": -10, "Default": 0, "Maximum": 10}}}
HEAD_IN = [("ParamAngleX", 60, "X"), ("ParamAngleZ", 60, "Angle"), ("ParamBodyAngleX", 40, "X"), ("ParamBodyAngleZ", 40, "Angle")]
BODY_IN = [("ParamBodyAngleX", 100, "X"), ("ParamBodyAngleZ", 100, "Angle")]
settings = [
    ("PhysicsSetting1", "앞머리", phys("PhysicsSetting1", HEAD_IN, [("ParamHairFront", 1, 1.3)], 2, 10, 0.95, 0.9, 1.5)),
    ("PhysicsSetting2", "옆머리", phys("PhysicsSetting2", HEAD_IN, [("ParamHairSide", 1, 1.6)], 2, 15, 0.95, 0.85, 1.4)),
    ("PhysicsSetting3", "뒷머리", phys("PhysicsSetting3", HEAD_IN, [("ParamHairBack", 1, 1.2)], 2, 18, 0.93, 0.85, 1.2)),
    ("PhysicsSetting4", "아호게", phys("PhysicsSetting4", HEAD_IN, [("ParamAhoge", 1, 2.0)], 2, 8, 0.97, 0.95, 1.8)),
    ("PhysicsSetting5", "마이크", phys("PhysicsSetting5", HEAD_IN, [("ParamMicSwing", 1, 0.8)], 2, 6, 0.9, 0.8, 1.0)),
    ("PhysicsSetting6", "후드끈", phys("PhysicsSetting6", BODY_IN, [("ParamDrawstring", 1, 1.5)], 2, 12, 0.95, 0.9, 1.5)),
    ("PhysicsSetting7", "밑단", phys("PhysicsSetting7", BODY_IN, [("ParamHem", 1, 0.9)], 2, 10, 0.9, 0.8, 1.0)),
    ("PhysicsSetting8", "소매", phys("PhysicsSetting8", BODY_IN, [("ParamSleeveR", 1, 0.8), ("ParamSleeveL", 1, -0.8)], 2, 14, 0.9, 0.85, 1.0)),
    ("PhysicsSetting9", "스트랩", phys("PhysicsSetting9", BODY_IN, [("ParamStrap", 1, 1.2)], 2, 12, 0.95, 0.9, 1.3)),
    ("PhysicsSetting10", "케이블", phys("PhysicsSetting10", BODY_IN, [("ParamCableSwingX", 2, 1.4), ("ParamCableSwingY", 1, 0.7)], 3, 16, 0.95, 0.8, 1.2)),
    ("PhysicsSetting11", "핍 안테나", phys("PhysicsSetting11", [("ParamPipX", 100, "X"), ("ParamPipY", 50, "Angle")], [("ParamPipAntenna", 1, 1.8)], 2, 6, 0.97, 0.95, 1.8)),
    ("PhysicsSetting12", "정령 링", phys("PhysicsSetting12", [("ParamAngleX", 50, "X"), ("ParamAngleZ", 50, "Angle")], [("ParamRingFloat", 1, 0.8)], 2, 20, 0.85, 0.6, 0.8)),
]
physics = {"Version": 3, "Meta": {"PhysicsSettingCount": len(settings),
                                  "TotalInputCount": sum(len(s[2]["Input"]) for s in settings),
                                  "TotalOutputCount": sum(len(s[2]["Output"]) for s in settings),
                                  "VertexCount": sum(len(s[2]["Vertices"]) for s in settings),
                                  "EffectiveForces": {"Gravity": {"X": 0, "Y": -1}, "Wind": {"X": 0, "Y": 0}},
                                  "PhysicsDictionary": [{"Id": s[0], "Name": s[1]} for s in settings]},
           "PhysicsSettings": [s[2] for s in settings]}
(EXP / "LTM_Lotium.physics3.json").write_text(json.dumps(physics, indent=1, ensure_ascii=False))

# ------------------------------------------------------------------ expressions (exp3.json)
EXPR = [
    ("exp_neutral", "기본", "F1", {}),
    ("exp_smile", "미소", "F2", {"ParamMouthForm": 1, "ParamEyeLSmile": 0.3, "ParamEyeRSmile": 0.3, "ParamCheek": 0.5}),
    ("exp_bigsmile", "활짝 웃음", "F3", {"ParamMouthForm": 1, "ParamMouthOpenY": 0.6, "ParamEyeLSmile": 1, "ParamEyeRSmile": 1, "ParamBlushStrong": 1, "ParamBrowLY": 0.4, "ParamBrowRY": 0.4}),
    ("exp_laugh", "크게 웃음", "F4", {"ParamMouthForm": 1, "ParamMouthOpenY": 1, "ParamEyeLSmile": 1, "ParamEyeRSmile": 1, "ParamBlushStrong": 1, "ParamBrowLY": 0.6, "ParamBrowRY": 0.6}),
    ("exp_mischievous", "장난기", "F5", {"ParamMouthForm": 1, "ParamEyeRSmile": 1, "ParamBrowLAngle": 0.5, "ParamEmoteHeart": 1}),
    ("exp_surprise", "놀람", "F6", {"ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0, "ParamEyeBallForm": -1, "ParamMouthOpenY": 0.6, "ParamMouthShape": -0.8, "ParamBrowLY": 1, "ParamBrowRY": 1}),
    ("exp_embarrassed", "당황", "F7", {"ParamBlushStrong": 1, "ParamMouthShape": -1, "ParamMouthOpenY": 0.2, "ParamEmoteSweat": 1, "ParamBrowLForm": -0.6, "ParamBrowRForm": -0.6}),
    ("exp_annoyed", "어이없음", "F8", {"ParamDeadpan": 1, "ParamMouthForm": -0.3, "ParamBrowLY": -0.3, "ParamBrowRY": 0.3}),
    ("exp_angry", "화남", "F9", {"ParamMouthForm": -1, "ParamShadowDark": 1, "ParamEmoteAnger": 1, "ParamBrowLAngle": -1, "ParamBrowRAngle": -1, "ParamBrowLY": -0.6, "ParamBrowRY": -0.6, "ParamEyeLOpen": 0.8, "ParamEyeROpen": 0.8}),
    ("exp_sad", "슬픔", "F10", {"ParamMouthForm": -0.8, "ParamEyeLOpen": 0.65, "ParamEyeROpen": 0.65, "ParamBrowLAngle": 1, "ParamBrowRAngle": 1, "ParamShadowDark": 0.5}),
    ("exp_cry", "울음", "F11", {"ParamTears": 1, "ParamMouthShape": -1, "ParamMouthOpenY": 0.25, "ParamMouthForm": -1, "ParamBrowLAngle": 1, "ParamBrowRAngle": 1, "ParamEyeLOpen": 0.75, "ParamEyeROpen": 0.75}),
    ("exp_sparkle", "방송 반짝", "F12", {"ParamEyeStar": 1, "ParamMouthForm": 1, "ParamMouthOpenY": 0.5, "ParamElectricFX": 1}),
    ("exp_glitch", "글리치", "Shift+F1", {"ParamGlitch": 1, "ParamMouthShape": -0.5}),
    ("exp_overclock", "오버클럭", "Shift+F2", {"ParamOverclock": 1, "ParamCoreGlow": 1, "ParamElectricFX": 1, "ParamMouthForm": 1, "ParamBrowLAngle": -0.4, "ParamBrowRAngle": -0.4}),
]
ABS = {"ParamEyeLOpen", "ParamEyeROpen"}
for fid, nm, key, pv in EXPR:
    assert all(k in PID for k in pv), (fid, pv)
    data = {"Type": "Live2D Expression", "FadeInTime": 0.25, "FadeOutTime": 0.25,
            "Parameters": [{"Id": k, "Value": v, "Blend": "Overwrite"} for k, v in pv.items()]}
    (EXP / "expressions" / f"{fid}.exp3.json").write_text(json.dumps(data, indent=1))

# cdi3 (display names) and model3 (references)
cdi = {"Version": 3,
       "Parameters": [{"Id": p["id"], "GroupId": "PG_" + p["group"], "Name": p["name"]} for p in P],
       "ParameterGroups": [{"Id": "PG_" + g, "GroupId": "", "Name": g} for g in dict.fromkeys(p["group"] for p in P)],
       "Parts": [{"Id": "Part_" + r["group"], "Name": r["group"]} for r in {r["group"]: r for r in rows}.values()]}
(EXP / "LTM_Lotium.cdi3.json").write_text(json.dumps(cdi, indent=1, ensure_ascii=False))
model3 = {"Version": 3, "FileReferences": {
    "Moc": "LTM_Lotium.moc3", "Textures": ["LTM_Lotium.4096/texture_00.png", "LTM_Lotium.4096/texture_01.png"],
    "Physics": "LTM_Lotium.physics3.json", "DisplayInfo": "LTM_Lotium.cdi3.json",
    "Expressions": [{"Name": fid, "File": f"expressions/{fid}.exp3.json"} for fid, *_ in EXPR],
    "Motions": {"Idle": [{"File": "motions/idle.motion3.json"}]}},
    "Groups": [{"Target": "Parameter", "Name": "EyeBlink", "Ids": ["ParamEyeLOpen", "ParamEyeROpen"]},
               {"Target": "Parameter", "Name": "LipSync", "Ids": ["ParamMouthOpenY"]}]}
(EXP / "LTM_Lotium.model3.json").write_text(json.dumps(model3, indent=1))

# idle motion (motion3.json): breath + sway + pip/ring float + core pulse, 4s loop
def curve(pid, pts):
    seg = [pts[0][0], pts[0][1]]
    for t, v in pts[1:]:
        seg += [0, t, v]  # linear segments
    return {"Target": "Parameter", "Id": pid, "Segments": seg}
dur = 4.0
curves = [curve("ParamBreath", [(0, 0), (2, 1), (4, 0)]),
          curve("ParamBodyAngleX", [(0, 0), (1, 1.5), (3, -1.5), (4, 0)]),
          curve("ParamAngleZ", [(0, 0), (1.5, 2), (3.5, -1), (4, 0)]),
          curve("ParamPipY", [(0, 0), (1, 0.6), (3, -0.6), (4, 0)]),
          curve("ParamPipX", [(0, 0), (2, 0.3), (4, 0)]),
          curve("ParamRingRotate", [(0, -0.2), (2, 0.2), (4, -0.2)]),
          curve("ParamCoreGlow", [(0, 0.45), (2, 0.6), (4, 0.45)])]
segcount = sum((len(c["Segments"]) - 2) // 3 for c in curves)
motion = {"Version": 3, "Meta": {"Duration": dur, "Fps": 30, "Loop": True, "AreBeziersRestricted": True,
                                 "CurveCount": len(curves), "TotalSegmentCount": segcount,
                                 "TotalPointCount": segcount + len(curves), "UserDataCount": 0, "TotalUserDataSize": 0},
          "Curves": curves}
(EXP / "motions").mkdir(exist_ok=True)
(EXP / "motions" / "idle.motion3.json").write_text(json.dumps(motion, indent=1))

json.dump({"rows": rows, "params": P, "expr": EXPR, "tree": dump(tree)}, open(OUT / "tools/_spec_cache.json", "w"), ensure_ascii=False)
print("layers", len(rows), "params", len(P), "physics", len(settings), "expressions", len(EXPR))
