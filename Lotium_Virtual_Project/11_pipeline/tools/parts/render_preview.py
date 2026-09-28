#!/usr/bin/env python3
"""Render composites of the part PNGs with toggle sets (QA of toggles/expressions).

Usage: python3 render_preview.py  -> 08_live2d_notes/qa_toggle_preview.png
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
MAN = json.loads((ROOT / "08_live2d_notes/parts_assembly_manifest.json").read_text())
LAY = sorted(MAN["layers"], key=lambda l: -l["z"])  # back -> front
CACHE = {}


def img(l):
    if l["name"] not in CACHE:
        CACHE[l["name"]] = np.array(Image.open(ROOT / "08_live2d_notes" / l["file"])).astype(np.float32) / 255
    return CACHE[l["name"]]


def render(show=(), hide=(), crop=None, bg=(0.93, 0.93, 0.95)):
    W, H = MAN["canvas"]["width"], MAN["canvas"]["height"]
    out = np.zeros((H, W, 3), np.float32)
    out[:] = bg
    for l in LAY:
        base = l["name"].split("_", 1)[1]
        vis = (l["visible"] or base in show) and base not in hide
        if not vis:
            continue
        a = img(l)
        y, x = l["y"], l["x"]
        h, w = a.shape[:2]
        reg = out[y:y + h, x:x + w]
        if l["blend"] == "add":
            out[y:y + h, x:x + w] = np.clip(reg + a[..., :3] * a[..., 3:], 0, 1)
        else:
            out[y:y + h, x:x + w] = reg * (1 - a[..., 3:]) + a[..., :3] * a[..., 3:]
    im = Image.fromarray((out * 255).astype(np.uint8))
    return im.crop(crop) if crop else im


HEADSET = ["Headset_Band", "Headset_Cup_R", "Headset_Cup_L", "Headset_Cup_Glow", "Headset_Mic"]
EYES_OPEN = [f"Eye_{s}_{p}" for s in "RL" for p in ("White", "Iris", "Pupil", "Highlight", "Lash_Upper", "Line_Lower")]
OC = ["OC_Ring_Outer", "Drone_Trail_OC", "OC_Warning_Panel", "OC_Spark_Front", "OC_Hair_Spark", "OC_Eye_Ring_R",
      "OC_Eye_Ring_L", "OC_Core_Burst", "OC_Body_Rimlight"]
SETS = [
    ("Default", (), ()),
    ("Smile (closed ^ + grin)", ["Eye_R_Closed_Smile", "Eye_L_Closed_Smile", "Eye_R_Lid_Skin", "Eye_L_Lid_Skin",
                                 "Mouth_Grin_Mischief", "Face_Blush_Strong"], EYES_OPEN),
    ("Headset OFF + mobile", ["Hair_Headset_Press", "Earpiece_Mobile", "UI_Mobile_Frame"], HEADSET),
    ("Crying / sad", ["Eye_Tears_Pool", "Tear_Stream", "Mouth_Wavy", "Face_Shadow_Dark"], ()),
    ("Overclock", OC + ["Eye_Star_Sparkle"], ()),
    ("Hood up + game visor", ["Hood_Up", "Hair_Back_Hood", "Visor_Game", "UI_Game_HUD"], ["Hair_Back_Base"]),
    ("Glitch + low battery", ["FX_Glitch_Overlay", "FX_Glitch_Block_1", "FX_Glitch_Block_2", "LowBattery_Dim",
                              "UI_Panel_L_Battery_Low", "UI_Signal_Low", "FX_Emote_Sweat"],
     ["UI_Panel_L_Battery", "UI_Panel_R_Signal"]),
    ("Deadpan + anger", ["Eye_Flat_Deadpan", "Mouth_Pout", "FX_Emote_Anger"], ()),
]

if __name__ == "__main__":
    head = (1000, 0, 2100, 1150)
    tiles = []
    for title, show, hide in SETS:
        t = render(show, hide, crop=head).resize((440, 460))
        tiles.append((title, t))
    full = render().resize((600, 900))
    sheet = Image.new("RGB", (600 + 4 * 440, 920), (255, 255, 255))
    sheet.paste(full, (0, 10))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for i, (title, t) in enumerate(tiles):
        x, y = 600 + (i % 4) * 440, (i // 4) * 460
        sheet.paste(t, (x, y))
        d.rectangle((x, y, x + 440, y + 24), fill=(20, 20, 30))
        d.text((x + 6, y + 6), title, fill=(255, 255, 255))
    sheet.save(ROOT / "08_live2d_notes/qa_toggle_preview.png")
    print("ok")
