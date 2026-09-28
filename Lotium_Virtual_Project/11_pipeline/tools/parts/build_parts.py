#!/usr/bin/env python3
"""Build Lotium Live2D part PNGs from the approved masters.

Sources (all generated in PHASE 6, see 03_concepts/masters):
  - LTM_FULLBODY_MASTER_v001.png : body, clothes, cable, Pip, spirit ring (upscaled x3)
  - LTM_FACE_MASTER_v001.png     : head (hair, face, eyes, mouth, headset), warped onto
                                   the fullbody head by a 3-landmark affine (eyes + chin)
  - LTM_ACCESSORY_MASTER_v001.png: hologram UI panels (keyed from dark background)
  - LTM_OVERCLOCK_MASTER_v001.png: warning panels, sparks, data fragments (keyed)
Hidden areas are restored by inpainting or by drawing with the locked palette.

Output: 08_parts/<category>/<NNN>_<Name>.png (cropped, transparent) and
        08_live2d_notes/parts_build.json (raw layer records for the manifests).
Canvas: 3072 x 4608 px.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from classes import BG, CREAM, CYAN, DARK, HAIR, ORANGE_DARK, SKIN, classify  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
M_DIR = ROOT / "03_concepts" / "masters"
OUT = ROOT / "08_parts"
S = 3
W, H = 1024 * S, 1536 * S

# ------------------------------------------------------------------ sources
fb_img = Image.open(M_DIR / "fullbody/LTM_FULLBODY_MASTER_v001.png").convert("RGB")
fb = np.array(fb_img)
fbU = np.array(fb_img.resize((W, H), Image.LANCZOS))
labB = classify(fb)
fm = np.array(Image.open(M_DIR / "face/LTM_FACE_MASTER_v001.png").convert("RGB"))
labF = classify(fm)
FMH, FMW = fm.shape[:2]

# affine face-master -> canvas (landmarks measured on both masters)
SRC = np.float32([[497, 565], [748, 568], [622, 866]])
DST = np.float32([[474.2 * S, 196.7 * S], [535.0 * S, 193.3 * S], [506.7 * S, 263.3 * S]])
AFF = cv2.getAffineTransform(SRC, DST)
fmC = cv2.warpAffine(fm, AFF, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

PAL = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in {
    "skin": "#FCE6D6", "skin_sh": "#EFB9A0", "blush": "#FF9C8A", "line": "#3A2418",
    "hair": "#FF8A1F", "hair_sh": "#D95F10", "hair_sh2": "#A8420A", "cream": "#F6EFE2",
    "cream_sh": "#D9C9B8", "black": "#1A1A1F", "black_hi": "#2E3346", "navy": "#20263A",
    "cyan": "#3FF2FF", "glow": "#EFFFFF", "warn": "#FF4A3D", "white": "#FFFFFF",
    "brow": "#B5561A", "tear": "#BFEFFF", "metal": "#C9CED8"}.items()}


# ------------------------------------------------------------------ helpers
def poly(shape, pts):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.int32(np.round(pts))], 1)
    return m.astype(bool)


def box(shape, x0, y0, x1, y1):
    m = np.zeros(shape[:2], bool)
    m[max(y0, 0):y1, max(x0, 0):x1] = True
    return m


def ellipse(shape, c, ax, ang=0):
    m = np.zeros(shape[:2], np.uint8)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (int(ax[0]), int(ax[1])), ang, 0, 360, 1, -1)
    return m.astype(bool)


def dil(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.dilate(m.astype(np.uint8), k).astype(bool)


def ero(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.erode(m.astype(np.uint8), k).astype(bool)


def close(m, r):
    return ero(dil(m, r), r)


def fill_holes(m):
    m8 = m.astype(np.uint8)
    ff = m8.copy()
    h, w = m8.shape
    msk = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, msk, (0, 0), 1)
    return m | (ff == 0)


def thin_dark(lab):
    d = lab == DARK
    return d & ~cv2.morphologyEx(d.astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)).astype(bool)


def inpaint(rgb, hole, r=5):
    return cv2.inpaint(rgb, hole.astype(np.uint8), r, cv2.INPAINT_TELEA)


def solid(shape, color):
    a = np.zeros(shape[:2] + (3,), np.uint8)
    a[:] = color
    return a


fgB = labB != BG
fgF = labF != BG
tdB, tdF = thin_dark(labB), thin_dark(labF)
hsvF = cv2.cvtColor(fm, cv2.COLOR_RGB2HSV)
vF, sF = hsvF[..., 2].astype(int), hsvF[..., 1].astype(int)

LAYERS = []  # records in back->front order


def add(name, group, cat, rgb, alpha, visible=True, blend="normal", toggle=False, physics=False,
        param="", hidden=False, src=""):
    """rgb/alpha at canvas resolution. alpha float 0..1."""
    alpha = np.clip(alpha, 0, 1).astype(np.float32)
    ys_, xs_ = np.where(alpha > 0.008)
    if len(ys_) == 0:
        print("EMPTY (skipped)", name)
        return
    y0, y1, x0, x1 = ys_.min(), ys_.max() + 1, xs_.min(), xs_.max() + 1
    rgb = np.ascontiguousarray(rgb[y0:y1, x0:x1])
    alpha = np.ascontiguousarray(alpha[y0:y1, x0:x1])
    LAYERS.append(dict(name=name, group=group, cat=cat, rgb=rgb, alpha=alpha, x0=int(x0), y0=int(y0), visible=visible,
                       blend=blend, toggle=toggle, physics=physics, param=param,
                       hidden_restored=hidden, source=src))


def from_fb(mask, rgb1x=None):
    """mask at fullbody 1x -> canvas alpha; colors from upscaled fullbody (or given 1x rgb)."""
    mask = mask | (dil(mask, 1) & fgB)  # 1px internal overlap: no seams between adjacent parts
    a = cv2.resize(mask.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    a = np.clip((cv2.GaussianBlur(a, (0, 0), 1.6) - 0.5) * 2.4 + 0.5, 0, 1)  # smooth 3x upscale stair-steps
    rgb = fbU if rgb1x is None else np.array(Image.fromarray(rgb1x).resize((W, H), Image.LANCZOS))
    return rgb, a


def from_fm(mask, rgbF=None):
    mask = mask | (dil(mask, 1) & fgF)
    a = cv2.warpAffine(mask.astype(np.float32), AFF, (W, H), flags=cv2.INTER_LINEAR)
    rgb = fmC if rgbF is None else cv2.warpAffine(rgbF, AFF, (W, H), flags=cv2.INTER_LINEAR,
                                                  borderMode=cv2.BORDER_REPLICATE)
    return rgb, a


def draw_fm(fn, ss=4):
    """draw in face-master space with supersampling; fn(draw, scale) -> RGBA fm-space arrays."""
    im = Image.new("RGBA", (FMW * ss, FMH * ss), (0, 0, 0, 0))
    fn(ImageDraw.Draw(im), ss)
    im = np.array(im.resize((FMW, FMH), Image.LANCZOS))
    return im[..., :3].copy(), im[..., 3] / 255.0


def fm_rgba_to_canvas(rgb, a):
    rgbC = cv2.warpAffine(rgb, AFF, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    aC = cv2.warpAffine(a.astype(np.float32), AFF, (W, H), flags=cv2.INTER_LINEAR)
    return rgbC, aC


def draw_canvas(fn, box_=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(ImageDraw.Draw(im))
    im = np.array(im)
    return im[..., :3].copy(), im[..., 3] / 255.0


def glow(rgb_color, mask_canvas, radius, strength=1.0):
    a = cv2.GaussianBlur(mask_canvas.astype(np.float32), (0, 0), radius) * strength
    return solid((H, W), rgb_color), np.clip(a, 0, 1)


def key_highpass(img, box_, color_filter=None, gain=60.0, blur=41):
    """cut a glowing element from a dark-background sheet. returns (rgb, alpha) of the box."""
    x0, y0, x1, y1 = box_
    c = img[y0:y1, x0:x1].astype(np.float32)
    lum = c.max(axis=2)
    a = np.clip((lum - 135) / 90, 0, 1) ** 1.3
    if color_filter is not None:
        a *= color_filter(c)
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    hh, ww = a.shape
    fy = np.clip(np.minimum(np.arange(hh), np.arange(hh)[::-1]) / 14.0, 0, 1)
    fx = np.clip(np.minimum(np.arange(ww), np.arange(ww)[::-1]) / 14.0, 0, 1)
    a *= fy[:, None] * fx[None, :]  # feather patch edges
    return c.astype(np.uint8), a


def paste(dst_shape, rgb, a, x, y, scale=1.0):
    """place a small rgba patch into a canvas-size layer at (x,y) top-left."""
    if scale != 1.0:
        rgb = cv2.resize(rgb, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        a = cv2.resize(a, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    R = np.zeros((H, W, 3), np.uint8)
    A = np.zeros((H, W), np.float32)
    h, w = a.shape
    R[y:y + h, x:x + w] = rgb
    A[y:y + h, x:x + w] = a
    return R, A


# ================================================================== BODY (fullbody master, 1x coords)
shapeB = fb.shape
headB = box(shapeB, 0, 0, 1024, 262)
ys_b, xs_b = np.mgrid[0:1536, 0:1024]

# --- separated floating items via components
# spirit ring arcs (cyan, top) -> 4 segments sorted left->right
ringcand = (labB == CYAN) & box(shapeB, 340, 0, 640, 130) & ~(box(shapeB, 385, 95, 625, 130))
ringcand = close(ringcand, 2)
n, cc, st, _ = cv2.connectedComponentsWithStats(ringcand.astype(np.uint8))
segs = sorted([i for i in range(1, n) if st[i, 4] > 120], key=lambda i: st[i, 0])
ring_all = np.zeros(shapeB[:2], bool)
for k, i in enumerate(segs):
    m = dil(cc == i, 2) & fgB
    ring_all |= m
    rgb, a = from_fb(m)
    add(f"Ring_Spirit_Seg{k + 1}", "01_BACK_FX", "effects", rgb, a, toggle=True,
        param="ParamRingRotate", src="FULLBODY")
rgbC_, aC_ = from_fb(ring_all)
r, a = glow(PAL["cyan"], aC_, 12, 0.9)
add("Ring_Spirit_Glow", "01_BACK_FX", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="derived:ring")

# OC outer ring (drawn, larger arcs behind head)
hc = (505 * S, 70 * S)


def _ocring(d):
    for a0, a1 in [(200, 250), (265, 330), (345, 390)]:
        d.arc((hc[0] - 190 * S, hc[1] - 60 * S, hc[0] + 190 * S, hc[1] + 60 * S), a0, a1,
              fill=PAL["cyan"] + (230,), width=5 * S)


r, a = draw_canvas(_ocring)
add("OC_Ring_Outer", "01_BACK_FX", "overclock", r, a, visible=False, blend="add", toggle=True,
    param="Tgl_Overclock", src="drawn")

# ================================================================== HEAD (face master space)
shapeF = fm.shape
headF = fgF & box(shapeF, 0, 0, FMW, 872)
face_oval = poly(shapeF, [(400, 420), (470, 385), (620, 372), (770, 385), (860, 420), (885, 560),
                          (872, 640), (842, 720), (762, 800), (682, 850), (622, 868), (560, 850),
                          (482, 800), (420, 720), (396, 640), (390, 560)])
eyeR_c, eyeL_c = (491, 566), (744, 567)        # eye openings (R = character right = viewer left)
irisR_c, irisL_c = (497, 565), (748, 568)
eyeR_box, eyeL_box = box(shapeF, 410, 505, 578, 606), box(shapeF, 662, 505, 832, 606)
mouth_poly = [(556, 731), (624, 729), (694, 731), (681, 748), (655, 764), (624, 770), (594, 764), (568, 748)]
mouth_box = box(shapeF, 545, 718, 706, 784)
nose_box = box(shapeF, 565, 612, 655, 706)
mark_box = box(shapeF, 748, 598, 802, 648)
features = eyeR_box | eyeL_box | mouth_box | nose_box | mark_box

# headset regions
cupR_box, cupL_box = box(shapeF, 252, 492, 412, 730), box(shapeF, 868, 485, 982, 725)
band_poly = poly(shapeF, [(300, 520), (322, 300), (395, 185), (515, 118), (645, 115), (645, 168),
                          (525, 172), (425, 236), (372, 330), (360, 520)])
mic_box = box(shapeF, 700, 675, 910, 815)
darkcy = (labF == DARK) | (labF == CYAN)
cupR = fill_holes(close(darkcy & cupR_box, 3)) & cupR_box
cupL = fill_holes(close(darkcy & cupL_box, 3)) & cupL_box
band = darkcy & band_poly & ~cupR
mic = darkcy & mic_box & ~cupL & (labF != HAIR)
headset_all = cupR | cupL | band | mic

skin_med = np.median(fm[(labF == SKIN) & face_oval & ~features], axis=0).astype(np.uint8)

# ---------------- hair masks (exclusive zones)
hairlike = (labF == HAIR) | (labF == ORANGE_DARK)
hair_lines = tdF & dil(hairlike, 3)
pale_out = headF & ~face_oval & ((labF == CREAM) | (labF == SKIN)) & ~headset_all  # pale strands
_ysF = np.mgrid[0:FMH, 0:FMW][0]
pale_out &= _ysF < 835  # below this the face master shows the hood, not hair
hair_lines &= (_ysF < 835) | dil(hairlike, 1)
hair_px = headF & (hairlike | hair_lines | pale_out | ((labF == CYAN) & ~headset_all)) & ~(features & ~hairlike) & ~headset_all
hair_px &= ~(mark_box & (labF == CYAN))
ys, xs = np.mgrid[0:FMH, 0:FMW]
zone = {}
zone["ahoge"] = hair_px & (ys < 112) & (xs > 500) & (xs < 800)
rest = hair_px & ~zone["ahoge"]
zone["center"] = rest & poly(shapeF, [(585, 468), (662, 468), (652, 642), (602, 642)])
rest &= ~zone["center"]
zone["templeR"] = rest & box(shapeF, 355, 415, 425, 650)
zone["templeL"] = rest & box(shapeF, 850, 415, 912, 650)
rest &= ~(zone["templeR"] | zone["templeL"])
frontzone = (xs >= 400) & (xs <= 880) & (ys < 720)
zone["frontR"] = rest & frontzone & (xs < 560)
zone["frontC"] = rest & frontzone & (xs >= 560) & (xs < 700)
zone["frontL"] = rest & frontzone & (xs >= 700)
rest &= ~frontzone
zone["backLower"] = rest & (xs >= 400) & (xs <= 880)
rest &= ~zone["backLower"]
zone["sideR_up"] = rest & (xs < 400) & (ys < 600)
zone["sideR_lo"] = rest & (xs < 400) & (ys >= 600)
zone["sideL_up"] = rest & (xs > 880) & (ys < 600)
zone["sideL_lo"] = rest & (xs > 880) & (ys >= 600)
cyan_streak = (labF == CYAN) & hair_px

hair_sil = fill_holes(close(hair_px | headset_all, 9)) & headF

# back hair base (restored silhouette behind face)
back_base = ero(hair_sil, 6) | (face_oval & ~ero(face_oval, 30))
back_rgb = np.zeros_like(fm)
grad = np.linspace(0, 1, FMH)[:, None, None]
back_rgb[:] = (np.array(PAL["hair_sh"]) * (1 - grad) + np.array(PAL["hair_sh2"]) * grad).astype(np.uint8)
r, a = from_fm(back_base, back_rgb)
add("Hair_Back_Base", "02_BACK_HAIR", "hair", r, a, physics=True, param="ParamHairBack", hidden=True,
    src="restored:FACE silhouette")
r, a = from_fm(dil(zone["backLower"], 1))
add("Hair_Back_Lower", "02_BACK_HAIR", "hair", r, a, physics=True, param="ParamHairBack", src="FACE")
# hood-down variant: flattened silhouette
hood_sil = back_base & (ys > 200)
r, a = from_fm(hood_sil, back_rgb)
add("Hair_Back_Hood", "02_BACK_HAIR", "hair", r, a, visible=False, toggle=True, param="Tgl_Hood",
    hidden=True, src="restored:FACE silhouette")

# ================================================================== BODY layers (03_BODY)
# cable centerline (1x)
cable_pts = [(645, 742), (655, 790), (676, 850), (700, 900), (724, 950), (744, 1000), (752, 1032)]
cable_band = np.zeros(shapeB[:2], np.uint8)
cv2.polylines(cable_band, [np.int32(cable_pts)], False, 1, 20)
cable_band = cable_band.astype(bool)
plug = box(shapeB, 728, 1025, 795, 1165) & fgB
cable = (cable_band & fgB & (labB != HAIR)) | plug
cable_up = cable & box(shapeB, 0, 0, 1024, 850)
cable_mid = cable & box(shapeB, 0, 850, 1024, 1025) & ~plug
cable_end = plug

# jacket / sleeve geometry
sleeve_bR = [(430, 318), (398, 470), (368, 600), (348, 700), (342, 800)]
sleeve_bL = [(598, 318), (636, 470), (660, 600), (680, 700), (692, 800)]
sleeveR_poly = poly(shapeB, [(150, 300)] + sleeve_bR + [(150, 800)])
sleeveL_poly = poly(shapeB, [(900, 300)] + sleeve_bL + [(900, 800)])
handR_box, handL_box = box(shapeB, 195, 738, 275, 872), box(shapeB, 738, 742, 822, 875)
cyanB = labB == CYAN
cuffR_poly = poly(shapeB, [(165, 688), (250, 688), (348, 742), (348, 805), (165, 805)])
cuffL_poly = poly(shapeB, [(690, 688), (865, 688), (865, 805), (700, 805), (686, 760)])
rimR = cyanB & cuffR_poly
rimL = cyanB & cuffL_poly
openR = fill_holes(close(rimR, 4)) & ~dil(rimR, 1)
openL = fill_holes(close(rimL, 4)) & ~dil(rimL, 1)
handR = fgB & handR_box & ~dil(rimR, 1) & ~(labB == CREAM) | (fgB & handR_box & (labB == SKIN))
handL = fgB & handL_box & ~dil(rimL, 1) & ~(labB == CREAM) | (fgB & handL_box & (labB == SKIN))
handR &= ~openR | (labB == SKIN) | (labB == DARK)
handL &= ~openL | (labB == SKIN) | (labB == DARK)
sleeveR = fgB & sleeveR_poly & box(shapeB, 0, 300, 1024, 805) & ~handR & ~headB
sleeveL = fgB & sleeveL_poly & box(shapeB, 0, 300, 1024, 805) & ~handL & ~headB
sleeveR &= ~box(shapeB, 0, 0, 1024, 300)
strapR = sleeveR & box(shapeB, 238, 352, 378, 600) & ((labB == HAIR) | (labB == ORANGE_DARK) | (labB == DARK) | tdB)
strapL = sleeveL & box(shapeB, 640, 390, 765, 635) & ((labB == HAIR) | (labB == ORANGE_DARK) | (labB == DARK) | tdB)
sleeveInR = sleeveR & openR
sleeveInL = sleeveL & openL
cuffR = sleeveR & cuffR_poly & ~sleeveInR & ~strapR
cuffL = sleeveL & cuffL_poly & ~sleeveInL & ~strapL
armR_up = sleeveR & (ys_b < 520) & ~strapR & ~cuffR & ~sleeveInR
armR_fo = sleeveR & ~armR_up & ~strapR & ~cuffR & ~sleeveInR
armL_up = sleeveL & (ys_b < 520) & ~strapL & ~cuffL & ~sleeveInL
armL_fo = sleeveL & ~armL_up & ~strapL & ~cuffL & ~sleeveInL

# drawstrings, core, inner, collar, hood
dsR = fgB & box(shapeB, 423, 333, 447, 530) & (labB != CREAM)
dsL = fgB & box(shapeB, 561, 333, 586, 530) & (labB != CREAM)
core_box = box(shapeB, 474, 350, 537, 416)
core_face = core_box & (labB == CYAN) & ellipse(shapeB, (505, 382), (24, 24))
core_case = core_box & fgB & ~core_face & ~(labB == CREAM)
inner_zone = poly(shapeB, [(468, 262), (552, 262), (552, 670), (468, 670)])
inner = fgB & inner_zone & ~core_case & ~core_face & ((labB == DARK) | (labB == CYAN) | tdB) & ~dsR & ~dsL
hood0 = fgB & box(shapeB, 372, 262, 662, 322) & ~inner_zone & ~sleeveR & ~sleeveL & ~(box(shapeB, 470, 240, 552, 280) & (labB == SKIN))
_hsv = cv2.cvtColor(fb, cv2.COLOR_RGB2HSV)
hood0 &= ~((_hsv[..., 1] > 60) & (_hsv[..., 0] >= 5) & (_hsv[..., 0] <= 35))  # drop hair-tip pixels (orange/yellow)
hood_back = poly(shapeB, [(392, 322), (398, 296), (425, 274), (462, 262), (560, 262), (598, 274), (628, 294), (650, 322)])
hood0 &= ~((labB == DARK) & ~tdB)  # inner black belongs to collar/torso, not the hood
_neckrect = poly(shapeB, [(471, 266), (549, 266), (549, 330), (471, 330)])
hood = fill_holes(close(hood0 | _neckrect, 12)) & box(shapeB, 372, 262, 662, 322) & ~inner_zone & ~_neckrect
hood_rgb = inpaint(fb, hood & ~hood0, 5)
_new = hood & ~hood0
hood_rgb[_new] = PAL["cream_sh"]  # redrawn hood lining behind the neck (flat, no smeared hair colours)
_top = hood & (ys_b < 300)
_hs = cv2.cvtColor(hood_rgb, cv2.COLOR_RGB2HSV)
_pale = _top & ((_hs[..., 2] > 235) | ((_hs[..., 1] > 45) & (_hs[..., 0] < 40)))  # leftover hair highlights/specks
hood_rgb[_pale] = PAL["cream_sh"]
hood_rgb = np.where(_top[..., None], cv2.medianBlur(hood_rgb, 5), hood_rgb).astype(np.uint8)
_edge = hood & ~ero(hood, 1) & (ys_b < 300) & _new
hood_rgb[_edge] = (138, 127, 119)
collar_poly = poly(shapeB, [(395, 300), (472, 300), (472, 372), (420, 372)]) | \
    poly(shapeB, [(548, 300), (630, 300), (608, 372), (548, 372)])
collar = fgB & collar_poly & ~dsR & ~dsL & ~sleeveR & ~sleeveL & ~hood
jfR_poly = poly(shapeB, sleeve_bR + [(472, 800), (472, 300)])
jfL_poly = poly(shapeB, [(548, 300), (548, 800)] + sleeve_bL[::-1])
jacketR = fgB & jfR_poly & box(shapeB, 0, 300, 1024, 800) & ~collar & ~dsR & ~sleeveR & ~inner_zone \
    & ~(labB == DARK) | (fgB & jfR_poly & tdB & box(shapeB, 0, 300, 1024, 800) & ~sleeveR & ~inner_zone)
jacketL = fgB & jfL_poly & box(shapeB, 0, 300, 1024, 800) & ~collar & ~dsL & ~sleeveL & ~inner_zone \
    & ~(labB == DARK) | (fgB & jfL_poly & tdB & box(shapeB, 0, 300, 1024, 800) & ~sleeveL & ~inner_zone)
# include black pocket tabs on jacket
jacketR |= fgB & jfR_poly & box(shapeB, 330, 560, 472, 800) & (labB == DARK) & ~sleeveR & (ys_b < 770)
jacketL |= fgB & jfL_poly & box(shapeB, 548, 560, 700, 800) & (labB == DARK) & ~sleeveL & (ys_b < 770)
jacketR &= ~collar
jacketL &= ~collar


def hem_of(m, depth=42):
    out = np.zeros_like(m)
    cols = np.where(m.any(0))[0]
    for x in cols:
        yy = np.where(m[:, x])[0]
        out[max(yy.max() - depth, 0):yy.max() + 1, x] = m[max(yy.max() - depth, 0):yy.max() + 1, x]
    return out


hemR, hemL = hem_of(jacketR), hem_of(jacketL)
jacketR &= ~hemR
jacketL &= ~hemL
hood_rim = cyanB & (hood | collar | jacketR | jacketL)

# pants, straps, shoes
jacket_all = jacketR | jacketL | hemR | hemL | sleeveR | sleeveL | collar
shoes = fgB & box(shapeB, 0, 1283, 1024, 1536)
pstrapR = fgB & box(shapeB, 344, 775, 384, 1005) & ((labB == HAIR) | (labB == ORANGE_DARK))
pstrapL = fgB & box(shapeB, 568, 672, 608, 1005) & ((labB == HAIR) | (labB == ORANGE_DARK))
pstrapR, pstrapL = dil(pstrapR, 1) & fgB, dil(pstrapL, 1) & fgB
pants_zone = box(shapeB, 318, 640, 710, 1300)
pants_vis = fgB & pants_zone & ~jacket_all & ~cable & ~shoes & ~handR & ~handL & ~pstrapR & ~pstrapL
pantsR_vis, pantsL_vis = pants_vis & (xs_b < 522), pants_vis & (xs_b >= 522)


def restore_hull(vis, extra_top=None):
    """restored full region = filled closed hull of visible part (+optional waist extension)."""
    full = fill_holes(close(vis, 12))
    if extra_top is not None:
        full |= extra_top
    return full


pantsR_full = restore_hull(pantsR_vis) & ~shoes
pantsL_full = restore_hull(pantsL_vis) & ~shoes
pants_rgb = inpaint(fb, (pantsR_full | pantsL_full) & ~(pantsR_vis | pantsL_vis), 7)

waist = poly(shapeB, [(430, 600), (600, 600), (612, 700), (418, 700)]) & ~(pantsR_vis | pantsL_vis)
torso = poly(shapeB, [(440, 330), (590, 330), (604, 690), (424, 690)])
lining = poly(shapeB, [(420, 285), (606, 285), (600, 700), (426, 700)])
neck_vis = fgB & box(shapeB, 470, 243, 552, 278) & (labB == SKIN)
neck_full = neck_vis | poly(shapeB, [(482, 252), (538, 252), (540, 300), (480, 300)])
neck_back = poly(shapeB, [(476, 250), (544, 250), (546, 300), (474, 300)])
armR_under = np.zeros(shapeB[:2], np.uint8)
cv2.polylines(armR_under, [np.int32([(408, 330), (360, 470), (300, 620), (242, 770)])], False, 1, 44)
armL_under = np.zeros(shapeB[:2], np.uint8)
cv2.polylines(armL_under, [np.int32([(618, 330), (668, 470), (726, 620), (778, 772)])], False, 1, 44)
sideR = poly(shapeB, [(430, 318), (385, 318), (350, 470), (318, 620), (300, 760), (345, 770)] + sleeve_bR[::-1][:0]) & ~jfR_poly
sideL = poly(shapeB, [(598, 318), (645, 318), (680, 470), (712, 620), (730, 760), (685, 770)]) & ~jfL_poly
# hidden-area restorations stay inside the master silhouette (covered in the default pose)
armR_under = armR_under.astype(bool) & fgB & (ys_b >= 332)
armL_under = armL_under.astype(bool) & fgB & (ys_b >= 332)
torso &= fgB
lining &= fgB
sideR &= fgB
sideL &= fgB
neck_back &= fgB
waist &= fgB

# ---- emit 03_BODY (back -> front)
port_rgb, port_a = draw_canvas(lambda d: (
    d.rounded_rectangle((632 * S, 700 * S, 668 * S, 748 * S), radius=6 * S, fill=PAL["black"] + (255,),
                        outline=PAL["cyan"] + (255,), width=2 * S)))
add("Cable_Port", "03_BODY", "accessories", port_rgb, port_a, param="ParamCable", hidden=True, src="drawn")
lin_rgb = solid(shapeB, PAL["black_hi"])  # dark lining: invisible through seams
r, a = from_fb(lining, lin_rgb)
add("Jacket_Back_Lining", "03_BODY", "clothes", r, a, param="ParamBodyAngleX", hidden=True, src="restored")
r, a = from_fb(hood, hood_rgb)
add("Hood_Folded", "03_BODY", "clothes", r, a, physics=True, toggle=True, param="Tgl_Hood", src="FULLBODY")
def _neck(back):
    def f(d, s):
        w = 14 if back else 0
        pts = [(572 - w, 780), (672 + w, 780), (682 + w, 900), (694 + w, 1010), (552 - w, 1010), (563 - w, 900)]
        if back:
            d.polygon([(x * s, y * s) for x, y in pts], fill=PAL["skin_sh"] + (255,))
            return
        # vertical gradient: shadowed under the chin, lighter toward the collar
        for k in range(46):
            y0 = 780 + k * 5
            c = tuple(int(PAL["skin_sh"][i] + (PAL["skin"][i] - PAL["skin_sh"][i]) * min(1, k / 18)) for i in range(3))
            d.rectangle((540 * s, y0 * s, 710 * s, (y0 + 5) * s), fill=c + (255,))
        mask = Image.new("L", d.im.size, 0)
        ImageDraw.Draw(mask).polygon([(x * s, y * s) for x, y in pts], fill=255)
        d.bitmap((0, 0), Image.eval(mask, lambda v: 255 - v), fill=(0, 0, 0, 0))
        # chin cast shadow (soft V under the jaw)
        d.polygon([(574 * s, 780 * s), (670 * s, 780 * s), (622 * s, 846 * s)], fill=PAL["skin_sh"] + (255,))
        for side in ([(572, 780), (563, 900), (552, 1010)], [(672, 780), (682, 900), (694, 1010)]):
            d.line([(x * s, y * s) for x, y in side], fill=(201, 143, 122, 255), width=3 * s, joint="curve")
    return f


def _neck_layer(back):
    im = Image.new("RGBA", (FMW * 4, FMH * 4 + 800), (0, 0, 0, 0))
    _neck(back)(ImageDraw.Draw(im), 4)
    arr = np.array(im.resize((FMW, FMH + 200), Image.LANCZOS))
    rgb, a = arr[..., :3].copy(), arr[..., 3] / 255.0
    rgbC = cv2.warpAffine(rgb, AFF, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    aC = cv2.warpAffine(a.astype(np.float32), AFF, (W, H), flags=cv2.INTER_LINEAR)
    return rgbC, aC


r, a = _neck_layer(True)
add("Neck_Back", "03_BODY", "body", r, a, param="ParamAngleZ", hidden=True, src="redrawn")
r, a = _neck_layer(False)
add("Neck", "03_BODY", "body", r, a, param="ParamAngleX/Y/Z", hidden=True, src="redrawn (clean neck + chin shadow)")
r, a = from_fb(waist, solid(shapeB, PAL["black"]))
add("Pants_Waist_Restore", "03_BODY", "clothes", r, a, param="ParamBodyAngleX", hidden=True, src="restored")
torso_rgb = solid(shapeB, PAL["black"])
torso_rgb[:, :, :] = (np.array(PAL["black"]) * 0.8 + np.array(PAL["black_hi"]) * 0.2).astype(np.uint8)
r, a = from_fb(torso, torso_rgb)
add("Torso_Restore", "03_BODY", "body", r, a, param="ParamBodyAngleX", hidden=True, src="restored")
inner_full = (fill_holes(close(inner, 6)) & inner_zone) | poly(shapeB, [(471, 266), (549, 266), (549, 330), (471, 330)])  # high neck redrawn where hair tips covered it
inner_rgb = fb.copy()
inner_rgb[inner_full & ~inner] = (28, 28, 34)  # redrawn black high-neck where hair covered it
inner_rgb = np.where((inner_full & ~inner)[..., None], cv2.GaussianBlur(inner_rgb, (0, 0), 2), inner_rgb).astype(np.uint8)
r, a = from_fb(inner_full, inner_rgb)
add("Inner_Body", "03_BODY", "clothes", r, a, param="ParamBreath", hidden=True, src="FULLBODY+restored")
circuit = inner & cyanB
_, ca = from_fb(circuit)
r, a = glow(PAL["cyan"], ca, 5, 1.2)
add("Inner_Circuit_Glow", "03_BODY", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="derived:inner cyan")
r, a = from_fb(dil(core_case, 1) & fgB & ~core_face)
add("Core_Case", "03_BODY", "accessories", r, a, param="ParamBreath", src="FULLBODY")
r, a = from_fb(core_face)
add("Core_Face", "03_BODY", "accessories", r, a, param="ParamBreath", src="FULLBODY")
_, ca = from_fb(core_face)
r, a = glow(PAL["glow"], ca, 18, 1.4)
add("Core_Glow", "03_BODY", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="derived:core")
for side, und in (("R", armR_under), ("L", armL_under)):
    m = und.astype(bool)
    rgb = solid(shapeB, PAL["black"])
    r, a = from_fb(m, rgb)
    add(f"Arm_{side}_Under", "03_BODY", "arms_hands", r, a, param=f"ParamArm{side}", hidden=True,
        src="restored:inner sleeve+wrist")
r, a = from_fb(sleeveInR)
add("Sleeve_R_Inner", "03_BODY", "clothes", r, a, param="ParamArmR", src="FULLBODY")
r, a = from_fb(sleeveInL)
add("Sleeve_L_Inner", "03_BODY", "clothes", r, a, param="ParamArmL", src="FULLBODY")
for side, hm in (("R", handR), ("L", handL)):
    glove = hm & ((labB == DARK) | tdB)
    skin_part = hm & (labB == SKIN)
    full = fill_holes(close(hm, 3))
    hrgb = fb.copy()
    hrgb[full & ~skin_part] = PAL["skin"]
    hrgb = inpaint(hrgb, full & ~skin_part & dil(skin_part, 4), 3)
    r, a = from_fb(full, hrgb)
    add(f"Hand_{side}", "03_BODY", "arms_hands", r, a, param=f"ParamHand{side}", hidden=True,
        src="FULLBODY+restored skin under glove")
    r, a = from_fb(dil(glove, 1) & hm)
    add(f"Hand_{side}_Glove", "03_BODY", "arms_hands", r, a, toggle=True, param="Tgl_Glove", src="FULLBODY")
r, a = from_fb(pantsR_full, pants_rgb)
add("Pants_R", "03_BODY", "legs", r, a, param="ParamLegR", hidden=True, src="FULLBODY+restored")
r, a = from_fb(pantsL_full, pants_rgb)
add("Pants_L", "03_BODY", "legs", r, a, param="ParamLegL", hidden=True, src="FULLBODY+restored")
r, a = from_fb(pstrapR)
add("Pants_Strap_R", "03_BODY", "legs", r, a, physics=True, param="ParamStrap", src="FULLBODY")
r, a = from_fb(pstrapL)
add("Pants_Strap_L", "03_BODY", "legs", r, a, physics=True, param="ParamStrap", src="FULLBODY")
r, a = from_fb(shoes & (xs_b < 525))
add("Shoe_R", "03_BODY", "legs", r, a, src="FULLBODY")
r, a = from_fb(shoes & (xs_b >= 525))
add("Shoe_L", "03_BODY", "legs", r, a, src="FULLBODY")
r, a = from_fb(cable_up)
add("Cable_Tail_Seg1", "03_BODY", "accessories", r, a, physics=True, param="ParamCable", src="FULLBODY")
r, a = from_fb(cable_mid)
add("Cable_Tail_Seg2", "03_BODY", "accessories", r, a, physics=True, param="ParamCable", src="FULLBODY")
r, a = from_fb(cable_end)
add("Cable_Tail_Plug", "03_BODY", "accessories", r, a, physics=True, param="ParamCable", src="FULLBODY")


def _ribbon(d):
    pts = []
    for i in range(len(cable_pts) - 1):
        (x0, y0), (x1, y1) = cable_pts[i], cable_pts[i + 1]
        for t in np.linspace(0, 1, 12, endpoint=False):
            pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    out = []
    for k, (x, y) in enumerate(pts):
        out.append(((x + 8 * math.sin(k * 0.45)) * S, y * S))
    d.line(out, fill=PAL["cyan"] + (120,), width=3 * S, joint="curve")


r, a = draw_canvas(_ribbon)
a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 2) * 0.8
add("Cable_Electric_Ribbon", "03_BODY", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="drawn")

# ================================================================== 04_CLOTHES
for side, poly_m, und in (("R", sideR, jfR_poly), ("L", sideL, jfL_poly)):
    r, a = from_fb(poly_m, solid(shapeB, PAL["cream_sh"]))
    add(f"Jacket_Side_Under_Arm_{side}", "04_CLOTHES", "clothes", r, a, param="ParamBodyAngleX",
        hidden=True, src="restored:jacket under sleeve")
for side, m in (("R", jacketR), ("L", jacketL)):
    r, a = from_fb(m)
    add(f"Jacket_Front_{side}", "04_CLOTHES", "clothes", r, a, param="ParamBodyAngleX", src="FULLBODY")
for side, m in (("R", hemR), ("L", hemL)):
    r, a = from_fb(m)
    add(f"Jacket_Hem_{side}", "04_CLOTHES", "clothes", r, a, physics=True, param="ParamHem", src="FULLBODY")
r, a = from_fb(collar)
add("Jacket_Collar", "04_CLOTHES", "clothes", r, a, param="ParamAngleX", src="FULLBODY")
_, ca = from_fb(hood_rim)
r, a = glow(PAL["cyan"], ca, 5, 1.0)
add("Jacket_Hood_Rim_Glow", "04_CLOTHES", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="derived:hood rim")
r, a = from_fb(dsR)
add("Drawstring_R", "04_CLOTHES", "clothes", r, a, physics=True, param="ParamDrawstring", src="FULLBODY")
r, a = from_fb(dsL)
add("Drawstring_L", "04_CLOTHES", "clothes", r, a, physics=True, param="ParamDrawstring", src="FULLBODY")
for side, up, fo, cu, st_ in (("R", armR_up, armR_fo, cuffR, strapR), ("L", armL_up, armL_fo, cuffL, strapL)):
    r, a = from_fb(up)
    add(f"Arm_{side}_Upper", "04_CLOTHES", "arms_hands", r, a, param=f"ParamArm{side}", src="FULLBODY")
    r, a = from_fb(fo)
    add(f"Arm_{side}_Forearm", "04_CLOTHES", "arms_hands", r, a, param=f"ParamArm{side}", src="FULLBODY")
    r, a = from_fb(cu)
    add(f"Sleeve_{side}_Cuff", "04_CLOTHES", "clothes", r, a, physics=True, param=f"ParamSleeve{side}",
        src="FULLBODY")
    r, a = from_fb(st_)
    add(f"Sleeve_{side}_Strap", "04_CLOTHES", "clothes", r, a, physics=True, param=f"ParamSleeve{side}",
        src="FULLBODY")
_, ca = from_fb(rimR | rimL)
r, a = glow(PAL["cyan"], ca, 7, 1.0)
add("Sleeve_Cuff_Glow", "04_CLOTHES", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="derived:cuff rims")

# ================================================================== 05_FACE
def _ear(cx, flip):
    def f(d, s):
        x0, y0, x1, y1 = (cx - 26) * s, 560 * s, (cx + 26) * s, 672 * s
        d.ellipse((x0, y0, x1, y1), fill=PAL["skin"] + (255,), outline=PAL["line"] + (255,), width=3 * s)
        ix = cx + (6 if flip else -6)
        d.arc(((ix - 12) * s, 585 * s, (ix + 12) * s, 650 * s), 100 if flip else -80, 260 if flip else 80,
              fill=PAL["skin_sh"] + (255,), width=4 * s)
    return f


for side, cx, fl in (("R", 380, False), ("L", 898, True)):
    rgb, a = draw_fm(_ear(cx, fl))
    r, a = fm_rgba_to_canvas(rgb, a)
    add(f"Ear_{side}", "05_FACE", "face", r, a, param="ParamAngleX", hidden=True, src="restored:drawn")

feat_tight = ellipse(shapeF, eyeR_c, (76, 36)) | ellipse(shapeF, eyeL_c, (76, 36)) | dil(poly(shapeF, mouth_poly), 5) | (mark_box & (labF == CYAN))
skin_clean = (labF == SKIN) & face_oval & ~feat_tight
face_full = face_oval | (dil(face_oval, 14) & (ys > 560) & (ys < 760) & ((xs < 470) | (xs > 800)))  # cheek-side extension only
tmp = fm.copy()
tmp[~face_full] = skin_med
hole = face_full & ~skin_clean
base_rgb = inpaint(tmp, hole, 9)
vS = vF.copy()
medv = int(np.median(vF[skin_clean]))
shadow = skin_clean & (vF < medv - 16)
base_rgb[shadow] = cv2.GaussianBlur(base_rgb, (0, 0), 6)[shadow]
jaw_line = tdF & dil(face_oval, 4) & ~ero(face_oval, 5) & (ys > 640)
base_rgb[jaw_line] = fm[jaw_line]
r, a = from_fm(face_full | jaw_line, base_rgb)
add("Face_Base", "05_FACE", "face", r, a, param="ParamAngleX/Y", hidden=True,
    src="FACE+restored forehead/eye sockets/sides")
r, a = from_fm(shadow)
add("Face_Shadow_Hair", "05_FACE", "face", r, a, param="ParamHairFront", src="FACE")
nose = nose_box & (np.abs(fm.astype(int) - skin_med.astype(int)).sum(2) > 28) & ~hairlike
r, a = from_fm(dil(nose, 1) & nose_box)
add("Nose", "05_FACE", "face", r, a, param="ParamAngleX", src="FACE")


def _blush(strong):
    def f(d, s):
        for cx in (470, 780):
            for k in range(10, 0, -1):
                al = int((70 if strong else 34) * (1 - k / 11))
                d.ellipse(((cx - 7 * k) * s, (650 - 3 * k) * s, (cx + 7 * k) * s, (650 + 3 * k) * s),
                          fill=PAL["blush"] + (al,))
            if strong:
                for j in range(3):
                    x = cx - 25 + j * 20
                    d.line(((x + 8) * s, 636 * s, (x - 4) * s, 664 * s), fill=(230, 90, 90, 200), width=3 * s)
    return f


for nm, st_ in (("Face_Blush", False), ("Face_Blush_Strong", True)):
    rgb, a = draw_fm(_blush(st_))
    r, a = fm_rgba_to_canvas(rgb, a)
    add(nm, "05_FACE", "face" if not st_ else "expressions", r, a, visible=not st_, toggle=st_,
        param="ParamCheek" if not st_ else "Exp", src="drawn")


def _shadow_dark(d, s):
    for k in range(40):
        y = 420 + k * 5
        al = int(110 * (1 - k / 40))
        d.rectangle((380 * s, y * s, 890 * s, (y + 5) * s), fill=(60, 40, 90, al))


rgb, a = draw_fm(_shadow_dark)
a = a * face_oval
r, a = fm_rgba_to_canvas(rgb, a)
add("Face_Shadow_Dark", "05_FACE", "expressions", r, a, visible=False, toggle=True, param="Exp", src="drawn")
mark = mark_box & (labF == CYAN)
r, a = from_fm(dil(mark, 1) & mark_box)
add("Face_Mark_Circuit", "05_FACE", "face", r, a, toggle=True, param="Tgl_FaceMark", src="FACE")

# ================================================================== 06_EYES
lash_col = PAL["line"]


def eye_layers(side, ec, ic, ebox):
    cx, cy = ec
    opening = ellipse(shapeF, ec, (70, 28))
    # white (restored full eyeball)
    ell = ellipse(shapeF, ec, (74, 32))
    lash0 = ebox & (vF < 110) & (ys < cy - 4) & ~hairlike
    low0 = ebox & (ys > cy + 14) & (vF < 205) & (labF != SKIN) & ~hairlike
    whiteish = ebox & (sF < 70) & (vF > 185) & ell
    irc0 = ellipse(shapeF, ic, (38, 38)) & ell
    openm = fill_holes(close(lash0 | low0 | whiteish | (irc0 & ~hairlike & (labF != SKIN)), 6)) & ell
    openm = openm & ~ero(lash0 | low0, 0) | (dil(openm, 3) & ell & (ys < cy))
    wr = np.zeros_like(fm)
    wr[:] = (250, 247, 245)
    topfrac = np.clip((ys - (cy - 30)) / 26.0, 0, 1)[..., None]
    wr = (np.array((224, 218, 234)) * (1 - topfrac) + np.array((250, 247, 245)) * topfrac).astype(np.uint8)
    r, a = from_fm(openm, wr)
    add(f"Eye_{side}_White", "06_EYES", "eyes", r, a, param=f"ParamEye{side}Open", hidden=True,
        src="restored:drawn eyeball")
    # iris (restored circle): mirror hidden top from bottom, inpaint highlights/pupil
    irc = ellipse(shapeF, ic, (38, 38))
    vis = irc & opening & ~((vF < 70) & (ys < ic[1] - 18))
    hi = irc & (vF > 232) & (sF < 45)
    pup = ellipse(shapeF, (ic[0], ic[1] + 2), (11, 24)) & (vF < 150)
    ir = fm.copy()
    miss = irc & ~vis
    yy, xx = np.where(miss)
    my = np.clip(2 * ic[1] - yy, 0, FMH - 1)
    ir[yy, xx] = fm[my, xx]
    ir = inpaint(ir, (hi | pup) & irc, 4)
    r, a = from_fm(irc, ir)
    add(f"Eye_{side}_Iris", "06_EYES", "eyes", r, a, param="ParamEyeBallX/Y", hidden=True,
        src="FACE+restored under lid")
    r, a = from_fm(dil(pup, 1) & irc)
    add(f"Eye_{side}_Pupil", "06_EYES", "eyes", r, a, param="ParamEyeBallX/Y", src="FACE")
    r, a = from_fm(dil(hi, 1) & irc)
    add(f"Eye_{side}_Highlight", "06_EYES", "eyes", r, a, param="ParamEyeBallX/Y", src="FACE")

    def _lid(d, s):
        d.ellipse(((cx - 76) * s, (cy - 36) * s, (cx + 76) * s, (cy + 34) * s), fill=tuple(int(c) for c in skin_med) + (255,))
    rgb, a = draw_fm(_lid)
    r, a = fm_rgba_to_canvas(rgb, a)
    add(f"Eye_{side}_Lid_Skin", "06_EYES", "eyes", r, a, visible=False, param=f"ParamEye{side}Open",
        hidden=True, src="restored:drawn lid")
    lash = ebox & (vF < 110) & (ys < cy - 4) & ~hairlike
    r, a = from_fm(dil(lash, 1) & ebox & ~hairlike)
    add(f"Eye_{side}_Lash_Upper", "06_EYES", "eyes", r, a, param=f"ParamEye{side}Open", src="FACE")
    low = ebox & (ys > cy + 14) & (vF < 205) & (labF != SKIN) & ~hairlike & ~irc
    r, a = from_fm(dil(low, 1) & ebox & ~hairlike)
    add(f"Eye_{side}_Line_Lower", "06_EYES", "eyes", r, a, param=f"ParamEye{side}Open", src="FACE")

    def _closed(d, s):
        d.arc(((cx - 66) * s, (cy - 30) * s, (cx + 66) * s, (cy + 16) * s), 20, 160, fill=lash_col + (255,), width=6 * s)
    rgb, a = draw_fm(_closed)
    r, a = fm_rgba_to_canvas(rgb, a)
    add(f"Eye_{side}_Closed_Line", "06_EYES", "eyes", r, a, visible=False, param=f"ParamEye{side}Open",
        src="drawn")

    def _smile(d, s):
        d.arc(((cx - 60) * s, (cy - 12) * s, (cx + 60) * s, (cy + 50) * s), 200, 340, fill=lash_col + (255,), width=7 * s)
    rgb, a = draw_fm(_smile)
    r, a = fm_rgba_to_canvas(rgb, a)
    add(f"Eye_{side}_Closed_Smile", "06_EYES", "expressions", r, a, visible=False, toggle=True,
        param=f"ParamEye{side}Smile", src="drawn")


eye_layers("R", eyeR_c, irisR_c, eyeR_box)
eye_layers("L", eyeL_c, irisL_c, eyeL_box)


def _stars(d, s):
    for (x, y) in (irisR_c, irisL_c):
        pts = []
        for k in range(8):
            rr = 30 if k % 2 == 0 else 9
            ang = -math.pi / 2 + k * math.pi / 4
            pts.append(((x + rr * math.cos(ang)) * s, (y + rr * math.sin(ang)) * s))
        d.polygon(pts, fill=(255, 246, 200, 255), outline=PAL["cyan"] + (255,))


rgb, a = draw_fm(_stars)
r, a = fm_rgba_to_canvas(rgb, a)
add("Eye_Star_Sparkle", "06_EYES", "expressions", r, a, visible=False, toggle=True, param="Tgl_EyeStar", src="drawn")


def _deadpan(d, s):
    for (x, y) in (eyeR_c, eyeL_c):
        d.rectangle(((x - 70) * s, (y - 30) * s, (x + 70) * s, (y - 2) * s), fill=tuple(int(c) for c in skin_med) + (255,))
        d.line(((x - 64) * s, (y - 2) * s, (x + 64) * s, (y - 2) * s), fill=lash_col + (255,), width=7 * s)


rgb, a = draw_fm(_deadpan)
r, a = fm_rgba_to_canvas(rgb, a)
add("Eye_Flat_Deadpan", "06_EYES", "expressions", r, a, visible=False, toggle=True, param="Exp", src="drawn")


def _tears_pool(d, s):
    for (x, y) in (eyeR_c, eyeL_c):
        d.ellipse(((x - 58) * s, (y + 8) * s, (x + 58) * s, (y + 32) * s), fill=PAL["tear"] + (150,))
        d.ellipse(((x - 20) * s, (y + 12) * s, (x - 6) * s, (y + 20) * s), fill=(255, 255, 255, 230))


rgb, a = draw_fm(_tears_pool)
r, a = fm_rgba_to_canvas(rgb, a)
add("Eye_Tears_Pool", "06_EYES", "expressions", r, a, visible=False, toggle=True, param="Exp", src="drawn")


def _tear_stream(d, s):
    for x0 in (eyeR_c[0] - 40, eyeL_c[0] + 40):
        d.line([(x0 * s, 596 * s), ((x0 - 4) * s, 660 * s), ((x0 + 2) * s, 740 * s)], fill=PAL["tear"] + (200,),
               width=9 * s, joint="curve")


rgb, a = draw_fm(_tear_stream)
r, a = fm_rgba_to_canvas(rgb, a)
add("Tear_Stream", "06_EYES", "expressions", r, a, visible=False, toggle=True, param="Exp", src="drawn")

# ================================================================== 07_BROWS (restored, hidden under bangs)
for side, pts in (("R", [(432, 503), (470, 494), (512, 490), (556, 492)]),
                  ("L", [(690, 492), (734, 490), (776, 494), (814, 503)])):
    def _brow(d, s, pts=pts):
        for w_, k in ((9, 0), (7, 1), (5, 2)):
            seg = pts[k:len(pts) - (2 - k) if k < 2 else len(pts)]
            d.line([(x * s, y * s) for x, y in seg], fill=PAL["brow"] + (255,), width=w_ * s, joint="curve")
    rgb, a = draw_fm(_brow)
    r, a = fm_rgba_to_canvas(rgb, a)
    add(f"Brow_{side}", "07_BROWS", "brows", r, a, param=f"ParamBrow{side}Y/Angle", hidden=True,
        src="restored:drawn (hidden by bangs in master)")

# ================================================================== 08_MOUTH
mpoly = poly(shapeF, mouth_poly)
mline_zone = dil(mpoly, 6) & mouth_box
mdark = mline_zone & (vF < 105)
teeth = mpoly & (sF < 45) & (vF > 205) & (ys < 748)
m_in = mpoly & ~mdark & ~teeth
tongue = m_in & (ys > 750) & (vF > 175)
inside = m_in & ~tongue
ins_rgb = fm.copy()
ins_full = mpoly
ins_rgb = inpaint(ins_rgb, (teeth | tongue) & mpoly, 4)
r, a = from_fm(ins_full, ins_rgb)
add("Mouth_Inside", "08_MOUTH", "mouth", r, a, param="ParamMouthOpenY", hidden=True, src="FACE+restored")
r, a = from_fm(dil(tongue, 1) & mpoly)
add("Mouth_Tongue", "08_MOUTH", "mouth", r, a, param="ParamMouthOpenY", src="FACE")


def _teeth_low(d, s):
    d.chord((582 * s, 748 * s, 666 * s, 790 * s), 200, 340, fill=(250, 250, 248, 255))


rgb, a = draw_fm(_teeth_low)
a = a * dil(mpoly, 2)
r, a = fm_rgba_to_canvas(rgb, a)
add("Mouth_Teeth_Lower", "08_MOUTH", "mouth", r, a, param="ParamMouthOpenY", hidden=True, src="restored:drawn")
r, a = from_fm(dil(teeth, 1) & mpoly)
add("Mouth_Teeth_Upper", "08_MOUTH", "mouth", r, a, param="ParamMouthOpenY", src="FACE")
r, a = from_fm(mdark & (ys < 742))
add("Mouth_Line_Upper", "08_MOUTH", "mouth", r, a, param="ParamMouthForm", src="FACE")
r, a = from_fm(mdark & (ys >= 742))
add("Mouth_Line_Lower", "08_MOUTH", "mouth", r, a, param="ParamMouthOpenY", src="FACE")


def _mouth_draw(kind):
    def f(d, s):
        sk = tuple(int(c) for c in skin_med) + (255,)
        # cover the open mouth with skin, then draw the variant
        d.polygon([(x * s, y * s) for x, y in [(548, 724), (700, 724), (700, 778), (548, 778)]], fill=sk)
        if kind == "closed":
            d.arc((586 * s, 712 * s, 664 * s, 752 * s), 25, 155, fill=lash_col + (255,), width=5 * s)
        elif kind == "pout":
            d.line([(598 * s, 744 * s), (612 * s, 738 * s), (624 * s, 745 * s), (636 * s, 738 * s), (650 * s, 744 * s)],
                   fill=lash_col + (255,), width=5 * s, joint="curve")
        elif kind == "grin":
            d.chord((566 * s, 716 * s, 684 * s, 776 * s), 0, 180, fill=(250, 250, 248, 255), outline=lash_col + (255,), width=5 * s)
            d.line((574 * s, 746 * s, 676 * s, 746 * s), fill=(200, 190, 190, 255), width=2 * s)
        elif kind == "wavy":
            pts = [((580 + i * 6) * s, (744 + 6 * math.sin(i * 1.1)) * s) for i in range(15)]
            d.line(pts, fill=lash_col + (255,), width=5 * s, joint="curve")
    return f


for nm, kind, vis_ in (("Mouth_Closed_Smile", "closed", False), ("Mouth_Pout", "pout", False),
                       ("Mouth_Grin_Mischief", "grin", False), ("Mouth_Wavy", "wavy", False)):
    rgb, a = draw_fm(_mouth_draw(kind))
    r, a = fm_rgba_to_canvas(rgb, a)
    add(nm, "08_MOUTH", "expressions", r, a, visible=vis_, toggle=True, param="ParamMouthForm/Exp", src="drawn")

# ================================================================== 09_HEADSET
band_full = dil(band, 1) & band_poly
r, a = from_fm(band_full)
add("Headset_Band", "09_HEADSET", "accessories", r, a, toggle=True, param="Tgl_Headset", src="FACE")
for side, cup in (("R", cupR), ("L", cupL)):
    crgb = inpaint(fm, cup & ~darkcy, 4)
    r, a = from_fm(cup, crgb)
    add(f"Headset_Cup_{side}", "09_HEADSET", "accessories", r, a, toggle=True, param="Tgl_Headset",
        hidden=True, src="FACE+restored under hair")
_, ca = from_fm((cupR | cupL) & (labF == CYAN))
r, a = glow(PAL["cyan"], ca, 6, 1.1)
add("Headset_Cup_Glow", "09_HEADSET", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="derived:earcup rings")
r, a = from_fm(dil(mic, 1) & mic_box & (labF != HAIR))
add("Headset_Mic", "09_HEADSET", "accessories", r, a, toggle=True, physics=True, param="Tgl_Mic", src="FACE")

# ================================================================== 10_FRONT_HAIR
hp = {"sideR_lo": ("Hair_Side_R_Lower", "ParamHairSide"), "sideL_lo": ("Hair_Side_L_Lower", "ParamHairSide"),
      "sideR_up": ("Hair_Side_R_Upper", "ParamHairSide"), "sideL_up": ("Hair_Side_L_Upper", "ParamHairSide"),
      "templeR": ("Hair_Temple_R", "ParamHairFront"), "templeL": ("Hair_Temple_L", "ParamHairFront"),
      "frontR": ("Hair_Front_R", "ParamHairFront"), "frontL": ("Hair_Front_L", "ParamHairFront"),
      "frontC": ("Hair_Front_C", "ParamHairFront"), "center": ("Hair_Front_Center_Strand", "ParamHairFront"),
      "ahoge": ("Hair_Front_Ahoge", "ParamAhoge")}
for key, (nm, prm) in hp.items():
    m = zone[key]
    r, a = from_fm(m)
    add(nm, "10_FRONT_HAIR", "hair", r, a, physics=True, param=prm, src="FACE")
_, ca = from_fm(cyan_streak)
r, a = glow(PAL["cyan"], ca, 5, 1.0)
add("Hair_Inner_Glow", "10_FRONT_HAIR", "effects", r, a, blend="add", toggle=True, param="Glow_Level",
    src="derived:hair cyan streak")
press = dil(band, 6) & hair_sil
prgb = inpaint(fm, press, 7)
r, a = from_fm(press, prgb)
add("Hair_Headset_Press", "10_FRONT_HAIR", "hair", r, a, visible=False, toggle=True, param="Tgl_Headset",
    hidden=True, src="restored:hair under band")

# ================================================================== 11_PIP
pip_zone = box(shapeB, 228, 128, 380, 282) & fgB & ~ring_all & ~(labB == CYAN) | (box(shapeB, 228, 128, 380, 282) & (labB == CYAN) & ~ring_all)
n, cc, st, _ = cv2.connectedComponentsWithStats(pip_zone.astype(np.uint8))
pip = np.zeros(shapeB[:2], bool)
hover = np.zeros(shapeB[:2], bool)
for i in range(1, n):
    if st[i, 4] < 40:
        continue
    comp = cc == i
    if st[i, 1] > 212 and st[i, 3] < 30:
        hover |= comp
    else:
        pip |= comp
hover = fgB & box(shapeB, 284, 279, 358, 304)
pip &= ~box(shapeB, 284, 279, 358, 304)
antenna = pip & ((labB == HAIR) | (labB == ORANGE_DARK) | (tdB & dil((labB == HAIR), 2))) & (ys_b < 210)
pip_eye = pip & cyanB
pip_body = pip & ~antenna
r, a = from_fb(hover)
add("Pip_Hover_Ring", "11_PIP", "pip", r, a, toggle=True, param="ParamDroneFloat", src="FULLBODY")
r, a = from_fb(pip_body)
add("Drone_Body", "11_PIP", "pip", r, a, toggle=True, param="ParamDroneFloat", src="FULLBODY")
r, a = from_fb(antenna)
add("Drone_Antenna", "11_PIP", "pip", r, a, toggle=True, physics=True, param="ParamDroneAntenna", src="FULLBODY")
r, a = from_fb(dil(pip_eye, 1) & pip)
add("Drone_Eye", "11_PIP", "pip", r, a, toggle=True, param="ParamDroneEye", src="FULLBODY")
_, ca = from_fb(pip_eye | hover)
r, a = glow(PAL["cyan"], ca, 9, 1.0)
add("Pip_Glow", "11_PIP", "effects", r, a, blend="add", toggle=True, param="Glow_Level", src="derived:pip")


def _trail(d):
    for k in range(4):
        d.arc(((150 + 8 * k) * S, (120 + 6 * k) * S, (330 - 8 * k) * S, (250 - 4 * k) * S), 200 + 10 * k, 330 - 10 * k,
              fill=PAL["cyan"] + (200 - 40 * k,), width=(4 - k) * S)


r, a = draw_canvas(_trail)
add("Drone_Trail_OC", "11_PIP", "overclock", r, a, visible=False, blend="add", toggle=True,
    param="Tgl_Overclock", src="drawn")

# ================================================================== 12_UI (keyed from accessory master)
acc = np.array(Image.open(M_DIR / "accessories/LTM_ACCESSORY_MASTER_v001.png").convert("RGB"))
cyanf = lambda c: np.clip(((c[..., 1] + c[..., 2]) / 2 - c[..., 0] - 10) / 60, 0, 1)
redf = lambda c: np.clip((c[..., 0] - (c[..., 1] + c[..., 2]) / 2 - 20) / 60, 0, 1)
anyf = lambda c: np.ones(c.shape[:2])
ui_items = [("UI_Panel_L_Battery", (1170, 765, 1325, 835), cyanf, (740, 330), True, "Tgl_UI"),
            ("UI_Panel_L_Battery_Low", (1352, 765, 1500, 835), anyf, (740, 330), False, "Tgl_LowBattery"),
            ("UI_Panel_R_Signal", (1170, 865, 1312, 978), cyanf, (160, 330), True, "Tgl_UI"),
            ("UI_Signal_Low", (1352, 865, 1490, 978), anyf, (160, 330), False, "Tgl_LowBattery"),
            ("UI_Mobile_Frame", (738, 760, 1125, 995), cyanf, (700, 420), False, "Tgl_Mobile")]
for nm, bx, flt, pos, vis_, prm in ui_items:
    c, a = key_highpass(acc, bx, flt, gain=45)
    r, a = paste((H, W), c, a, pos[0] * S, pos[1] * S, scale=S * 0.5)
    add(nm, "12_UI", "ui", r, a, visible=vis_, blend="add", toggle=True, param=prm, src="ACCESSORY keyed")


def _hud(d):
    x0, y0, x1, y1 = 330 * S, 150 * S, 700 * S, 250 * S
    d.rounded_rectangle((x0, y0, x1, y1), radius=10 * S, outline=PAL["cyan"] + (200,), width=2 * S)
    for k in range(6):
        d.rectangle((x0 + (20 + 34 * k) * S, y1 - 30 * S, x0 + (44 + 34 * k) * S, y1 - 16 * S), fill=PAL["cyan"] + (170,))
    d.line((x0 + 10 * S, y0 + 20 * S, x0 + 120 * S, y0 + 20 * S), fill=PAL["cyan"] + (200,), width=3 * S)


r, a = draw_canvas(_hud)
add("UI_Game_HUD", "12_UI", "ui", r, a, visible=False, blend="add", toggle=True, param="Tgl_Game", src="drawn")

# ================================================================== composite helper for derived FX
def composite(visible_only=True):
    out = np.zeros((H, W, 3), np.float32)
    for L in LAYERS:
        if visible_only and not L["visible"]:
            continue
        a = L["alpha"][..., None]
        y0, x0 = L["y0"], L["x0"]
        h, w = a.shape[:2]
        reg = out[y0:y0 + h, x0:x0 + w]
        if L["blend"] == "add":
            out[y0:y0 + h, x0:x0 + w] = np.clip(reg + L["rgb"] * a, 0, 255)
        else:
            out[y0:y0 + h, x0:x0 + w] = reg * (1 - a) + L["rgb"] * a
    return out.astype(np.uint8)


body_sil = np.zeros((H, W), np.float32)
for L in LAYERS:
    if L["visible"] and L["blend"] == "normal" and L["group"] in ("03_BODY", "04_CLOTHES", "05_FACE", "10_FRONT_HAIR", "09_HEADSET", "02_BACK_HAIR"):
        h, w = L["alpha"].shape
        body_sil[L["y0"]:L["y0"] + h, L["x0"]:L["x0"] + w] = np.maximum(
            body_sil[L["y0"]:L["y0"] + h, L["x0"]:L["x0"] + w], L["alpha"])
comp = composite()

# ================================================================== 13_FRONT_FX


def _sparkle(d):
    for (x, y, rr) in ((380, 110, 18), (640, 150, 14), (620, 60, 10), (400, 250, 12), (680, 260, 16)):
        x, y, rr = x * S, y * S, rr * S
        d.polygon([(x, y - rr), (x + rr * 0.25, y - rr * 0.25), (x + rr, y), (x + rr * 0.25, y + rr * 0.25),
                   (x, y + rr), (x - rr * 0.25, y + rr * 0.25), (x - rr, y), (x - rr * 0.25, y - rr * 0.25)],
                  fill=(255, 250, 220, 235))


r, a = draw_canvas(_sparkle)
add("FX_Sparkle_Front", "13_FRONT_FX", "effects", r, a, visible=False, blend="add", toggle=True,
    param="Tgl_EyeStar", src="drawn")
head_box = (380 * S, 40 * S, 640 * S, 300 * S)
gl = np.zeros((H, W, 3), np.uint8)
ga = np.zeros((H, W), np.float32)
x0, y0, x1, y1 = head_box
sub = comp[y0:y1, x0:x1].astype(np.int32)
shift = 14
redc = np.roll(sub[..., 0], shift, axis=1)
bluc = np.roll(sub[..., 2], -shift, axis=1)
diff = np.zeros_like(sub)
diff[..., 0] = np.clip(redc - sub[..., 0], 0, 255)
diff[..., 2] = np.clip(bluc - sub[..., 2], 0, 255)
gl[y0:y1, x0:x1] = diff.astype(np.uint8)
ga[y0:y1, x0:x1] = np.clip(diff.max(2) / 120.0, 0, 1)
bands = np.zeros(ga.shape, bool)
for k in range(0, y1 - y0, 36):
    if (k // 36) % 3 == 0:
        bands[y0 + k:y0 + k + 14, x0:x1] = True
ga *= bands
add("FX_Glitch_Overlay", "13_FRONT_FX", "effects", gl, ga, visible=False, blend="add", toggle=True,
    param="Tgl_Glitch", src="derived:RGB split of head")
for k, (bx, by, bw, bh, dx) in enumerate(((420, 150, 90, 18, 24), (500, 205, 110, 14, -30))):
    R_ = np.zeros((H, W, 3), np.uint8)
    A_ = np.zeros((H, W), np.float32)
    X, Y, BW, BH, DX = bx * S, by * S, bw * S, bh * S, dx * S
    R_[Y:Y + BH, X + DX:X + DX + BW] = comp[Y:Y + BH, X:X + BW]
    A_[Y:Y + BH, X + DX:X + DX + BW] = 0.9
    add(f"FX_Glitch_Block_{k + 1}", "13_FRONT_FX", "effects", R_, A_, visible=False, toggle=True,
        param="Tgl_Glitch", src="derived:displaced slice")

# ================================================================== 14_EXPRESSIONS (emotes, drawn)


def _heart(d):
    x, y, s_ = 660 * S, 110 * S, 22 * S
    d.ellipse((x - s_, y - s_, x, y), fill=(255, 110, 140, 240))
    d.ellipse((x, y - s_, x + s_, y), fill=(255, 110, 140, 240))
    d.polygon([(x - s_, y - s_ / 2), (x + s_, y - s_ / 2), (x, y + s_)], fill=(255, 110, 140, 240))


def _sweat(d):
    x, y = 640 * S, 150 * S
    d.polygon([(x, y - 26 * S), (x + 14 * S, y), (x - 14 * S, y)], fill=(170, 230, 255, 230))
    d.ellipse((x - 14 * S, y - 12 * S, x + 14 * S, y + 16 * S), fill=(170, 230, 255, 230))


def _anger(d):
    x, y = 640 * S, 120 * S
    for ang in (0, 90, 180, 270):
        a0 = math.radians(ang)
        cx, cy = x + 12 * S * math.cos(a0 + math.pi / 4), y + 12 * S * math.sin(a0 + math.pi / 4)
        d.arc((cx - 12 * S, cy - 12 * S, cx + 12 * S, cy + 12 * S), ang + 90, ang + 180, fill=PAL["warn"] + (255,), width=4 * S)


for nm, fn in (("FX_Emote_Heart", _heart), ("FX_Emote_Sweat", _sweat), ("FX_Emote_Anger", _anger)):
    r, a = draw_canvas(fn)
    add(nm, "14_EXPRESSIONS", "expressions", r, a, visible=False, toggle=True, param="Tgl_Emote", src="drawn")

# ================================================================== 15_TOGGLES
sil_head = cv2.warpAffine(hair_sil.astype(np.float32), AFF, (W, H)) > 0.5
face_c = cv2.warpAffine((face_oval | zone["frontR"] | zone["frontC"] | zone["frontL"] | zone["center"]).astype(np.float32), AFF, (W, H)) > 0.5
eye_y = int(195 * S)
hood_up = dil(sil_head, 18) & ~dil(face_c, 14) & (np.mgrid[0:H, 0:W][0] < eye_y + 40 * S)
hood_rgb = solid((H, W), PAL["cream"])
edge = hood_up & ~ero(hood_up, 6)
hood_rgb[edge] = PAL["cyan"]
yy = np.mgrid[0:H, 0:W][0]
shade = hood_up & (yy > 210 * S)
hood_rgb[shade & ~edge] = PAL["cream_sh"]
add("Hood_Up", "09_HEADSET", "clothes", hood_rgb, hood_up.astype(np.float32), visible=False, toggle=True,
    param="Tgl_Hood", src="drawn from head silhouette")


def _visor(d, s):
    d.rounded_rectangle((372 * s, 512 * s, 890 * s, 618 * s), radius=40 * s, fill=PAL["cyan"] + (80,),
                        outline=PAL["cyan"] + (230,), width=4 * s)
    for k in range(5):
        d.line((400 * s, (530 + 18 * k) * s, 860 * s, (530 + 18 * k) * s), fill=(255, 255, 255, 40), width=2 * s)


rgb, a = draw_fm(_visor)
r, a = fm_rgba_to_canvas(rgb, a)
add("Visor_Game", "15_TOGGLES", "accessories", r, a, visible=False, toggle=True, param="Tgl_Game", src="drawn")


def _earpiece(d, s):
    d.ellipse((885 * s, 590 * s, 925 * s, 650 * s), fill=PAL["black"] + (255,), outline=PAL["cyan"] + (255,), width=3 * s)
    d.ellipse((898 * s, 610 * s, 912 * s, 624 * s), fill=PAL["cyan"] + (255,))


rgb, a = draw_fm(_earpiece)
r, a = fm_rgba_to_canvas(rgb, a)
add("Earpiece_Mobile", "15_TOGGLES", "accessories", r, a, visible=False, toggle=True, param="Tgl_Mobile", src="drawn")
add("LowBattery_Dim", "15_TOGGLES", "effects", solid((H, W), PAL["navy"]), body_sil * 0.35, visible=False,
    toggle=True, param="Tgl_LowBattery", src="derived:body silhouette")

# ================================================================== 16_OVERCLOCK
oc = np.array(Image.open(M_DIR / "overclock/LTM_OVERCLOCK_MASTER_v001.png").convert("RGB"))
ocl = classify(oc)
bgc = np.median(oc[:40, :40].reshape(-1, 3), axis=0)
far = np.abs(oc.astype(int) - bgc).sum(2) > 60
n, cc, st, _ = cv2.connectedComponentsWithStats(far.astype(np.uint8))
fig = np.zeros(far.shape, bool)
if n > 1:
    big = 1 + np.argmax(st[1:, 4])
    fig = dil(cc == big, 6)
red_m = far & (oc[..., 0].astype(int) - oc[..., 2] > 60) & ~fig
cy_m = far & ~fig & ~red_m & (oc[..., 2].astype(int) > 150)
for nm, m in (("OC_Warning_Panel", dil(red_m, 2)), ("OC_Spark_Front", cy_m)):
    a = cv2.resize(m.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    lum = cv2.resize(oc.max(2).astype(np.float32), (W, H)) / 255.0
    a = a * np.clip(lum * 1.3, 0, 1)
    rgb = np.array(Image.fromarray(oc).resize((W, H), Image.LANCZOS))
    add(nm, "16_OVERCLOCK", "overclock", rgb, a, visible=False, blend="add", toggle=True,
        param="Tgl_Overclock", src="OVERCLOCK keyed")
hs = cv2.warpAffine(hair_sil.astype(np.float32), AFF, (W, H)) > 0.5
hedge = hs & ~ero(hs, 10) & (yy < 250 * S)
hedge &= (yy < 150 * S)
r, a = glow(PAL["cyan"], hedge.astype(np.float32), 5, 0.6)
add("OC_Hair_Spark", "16_OVERCLOCK", "overclock", r, a, visible=False, blend="add", toggle=True,
    param="Tgl_Overclock", src="derived:hair silhouette")


def _ocring_eye(c):
    def f(d, s):
        x, y = c
        for rr, w_ in ((34, 4), (24, 3)):
            d.ellipse(((x - rr) * s, (y - rr) * s, (x + rr) * s, (y + rr) * s), outline=PAL["cyan"] + (255,), width=w_ * s)
    return f


for side, c in (("R", irisR_c), ("L", irisL_c)):
    rgb, a = draw_fm(_ocring_eye(c))
    a = a * ellipse(shapeF, c, (40, 40))
    r, a = fm_rgba_to_canvas(rgb, a)
    add(f"OC_Eye_Ring_{side}", "16_OVERCLOCK", "overclock", r, a, visible=False, blend="add", toggle=True,
        param="Tgl_Overclock", src="drawn")
cm = np.zeros((H, W), np.float32)
cv2.circle(cm, (505 * S, 382 * S), 16 * S, 1.0, -1)
r, a = glow(PAL["glow"], cm, 24, 1.0)
add("OC_Core_Burst", "16_OVERCLOCK", "overclock", r, a, visible=False, blend="add", toggle=True,
    param="Tgl_Overclock", src="drawn")
bs = body_sil > 0.5
rim = bs & ~ero(bs, 5)
r, a = glow(PAL["cyan"], rim.astype(np.float32), 3, 0.7)
add("OC_Body_Rimlight", "16_OVERCLOCK", "overclock", r, a, visible=False, blend="add", toggle=True,
    param="Tgl_Overclock", src="derived:body silhouette (thin)")

# ================================================================== write
if __name__ == "__main__":
    out_json = []
    LAYERS.sort(key=lambda L: L["group"])  # stable: group order (01 back .. 16 front), then creation order
    n = len(LAYERS)
    seen = {}
    for idx, L in enumerate(LAYERS):
        lid = n - idx  # 001 = frontmost
        a8 = (L["alpha"] * 255).astype(np.uint8)
        y0, x0 = L["y0"], L["x0"]
        y1, x1 = y0 + a8.shape[0], x0 + a8.shape[1]
        rgba = np.dstack([L["rgb"], a8])
        rgba[rgba[..., 3] == 0, :3] = 0
        h = hashlib.sha256(rgba.tobytes()).hexdigest()
        if h in seen:
            print("DUP", L["name"], seen[h])
        seen[h] = L["name"]
        fname = f"{lid:03d}_{L['name']}.png"
        d = OUT / L["cat"]
        d.mkdir(parents=True, exist_ok=True)
        Image.fromarray(rgba, "RGBA").save(d / fname, optimize=True)
        out_json.append(dict(id=f"{lid:03d}", name=f"{lid:03d}_{L['name']}", group=L["group"],
                             file=f"08_parts/{L['cat']}/{fname}", x=int(x0), y=int(y0), w=int(x1 - x0),
                             h=int(y1 - y0), z=lid, visible=L["visible"], blend=L["blend"], toggle=L["toggle"],
                             physics=L["physics"], param=L["param"], hidden_restored=L["hidden_restored"],
                             source=L["source"], opaque_px=int((a8 > 128).sum())))
    (ROOT / "08_live2d_notes" / "parts_build.json").write_text(json.dumps(out_json, indent=1))
    Image.fromarray(composite()).save(ROOT / "08_live2d_notes" / "parts_composite_preview.png")
    print("layers", len(out_json))
