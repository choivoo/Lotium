#!/usr/bin/env python3
"""Export half-resolution parts + rig.json for the web rig from parts_assembly_manifest.json."""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
M = json.loads((ROOT / "08_live2d_notes/parts_assembly_manifest.json").read_text())
OUT = ROOT / "12_rig/web"
SC = 0.5
HEAD_G = {"02_BACK_HAIR", "05_FACE", "06_EYES", "07_BROWS", "08_MOUTH", "09_HEADSET", "10_FRONT_HAIR"}
HEAD_EXTRA = {"Visor_Game", "Earpiece_Mobile", "FX_Glitch_Overlay", "FX_Glitch_Block_1", "FX_Glitch_Block_2",
              "FX_Sparkle_Front", "FX_Emote_Heart", "FX_Emote_Sweat", "FX_Emote_Anger", "OC_Hair_Spark",
              "OC_Eye_Ring_R", "OC_Eye_Ring_L", "Ring_Spirit_Seg1", "Ring_Spirit_Seg2", "Ring_Spirit_Seg3",
              "Ring_Spirit_Seg4", "Ring_Spirit_Glow", "OC_Ring_Outer"}
DEPTH = [("Hair_Back", -0.5), ("Hood_Up", -0.25), ("Ear_", -0.3), ("Ring_", -0.6), ("OC_Ring", -0.6), ("Face_Base", 0),
         ("Face_Shadow_Hair", 0.05), ("Face_", 0.2), ("Eye_", 0.35), ("Tear", 0.35), ("OC_Eye", 0.35), ("Brow", 0.45),
         ("Nose", 0.55), ("Mouth", 0.35), ("Headset_Band", 0.1), ("Headset_Cup", 0.15), ("Headset_Mic", 0.5),
         ("Hair_Side", 0.3), ("Hair_Temple", 0.6), ("Hair_Front_Center", 0.9), ("Hair_Front_Ahoge", 0.4),
         ("Hair_Front", 0.8), ("Hair_Inner", 0.3), ("Hair_Headset", 0.1), ("Visor", 0.7), ("Earpiece", 0.15),
         ("FX_", 0.9), ("OC_Hair", 0.5)]
PHYS = {"Hair_Front_Ahoge": (0.16, "bottom"), "Hair_Front_Center_Strand": (0.09, "top"), "Hair_Front": (0.05, "top"),
        "Hair_Temple": (0.08, "top"), "Hair_Side": (0.07, "top"), "Hair_Back": (0.04, "top"), "Drawstring": (0.10, "top"),
        "Jacket_Hem": (0.025, "top"), "Sleeve_R_Cuff": (0.02, "top"), "Sleeve_L_Cuff": (0.02, "top"),
        "Sleeve_R_Strap": (0.05, "top"), "Sleeve_L_Strap": (0.05, "top"), "Pants_Strap": (0.05, "top"),
        "Cable_Tail_Seg1": (0.03, "top"), "Cable_Tail_Seg2": (0.06, "top"), "Cable_Tail_Plug": (0.09, "top"),
        "Drone_Antenna": (0.18, "bottom"), "Headset_Mic": (0.04, "right"), "Hood_Folded": (0.02, "top")}


def depth(n):
    return next((d for p, d in DEPTH if n.startswith(p)), 0.2)


out = []
(OUT / "parts").mkdir(parents=True, exist_ok=True)
for l in sorted(M["layers"], key=lambda l: -l["z"]):
    base = l["name"].split("_", 1)[1]
    im = Image.open(ROOT / "08_live2d_notes" / l["file"])
    w, h = max(1, round(im.width * SC)), max(1, round(im.height * SC))
    fn = f"parts/{l['id']}.png"
    im.resize((w, h), Image.LANCZOS).save(OUT / fn, optimize=True)
    x, y = l["x"] * SC, l["y"] * SC
    node = "head" if (l["group"] in HEAD_G or base in HEAD_EXTRA) else "body"
    if re.match(r"(Arm_R|Sleeve_R|Hand_R)", base):
        node = "armR"
    if re.match(r"(Arm_L|Sleeve_L|Hand_L)", base):
        node = "armL"
    if base.startswith(("Drone", "Pip")):
        node = "pip"
    if base.startswith("UI_"):
        node = "float"
    ph = None
    for k, (amp, where) in PHYS.items():
        if base.startswith(k):
            px = {"top": (x + w / 2, y), "bottom": (x + w / 2, y + h), "right": (x + w, y + h / 2)}[where]
            ph = {"amp": amp, "pivot": [round(px[0], 1), round(px[1], 1)]}
            break
    out.append(dict(n=base, f=fn, x=round(x, 1), y=round(y, 1), w=w, h=h, g=l["group"], vis=l["visible"],
                    add=l["blend"] == "add", node=node, d=depth(base) if node == "head" else 0, ph=ph))
rig = {"W": 1536, "H": 2304, "headPivot": [760, 400], "waist": [760, 1050], "shoulderR": [607, 495],
       "shoulderL": [925, 495], "layers": out}
(OUT / "rig.json").write_text(json.dumps(rig, separators=(",", ":")))
print("web parts", len(out))
