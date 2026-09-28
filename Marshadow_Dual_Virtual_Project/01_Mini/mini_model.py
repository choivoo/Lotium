"""MINI MARSHADOW — mascot Live2D model definition (NORMAL <-> SHADOW FIGHTING).
Fan-art mascot model (Pokémon-style silhouette by request). L = viewer's left.
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '03_Shared_Tools'))
from partkit import Part, hexc, ellipse_pts, mirror, band, shift, arc_pts, catmull, scale  # noqa

W, H, CX = 3000, 3600, 1500
MODEL = dict(code='MSM', title='Mini Marshadow Live2D', W=W, H=H, root=HERE,
             psd='Marshadow_Mini_Live2D_Master_v001.psd', default_state='NORMAL',
             face_box=(1000, 950, 2000, 1600), body_box=(1000, 1800, 2000, 2900), min_restore=8,
             groups=['00_GUIDE', '01_BACK_FX', '02_LOWER_SHADOW', '03_BODY', '04_ARMS', '05_SCARF',
                     '06_HEAD', '07_FACE', '08_EYES', '09_MARKS', '10_MOUTH', '11_FRONT_FX', '12_COMBAT'],
             guide_hidden_groups=[])

# palette -----------------------------------------------------------------
LINE = hexc('16171b')
HEAD_T, HEAD_B = hexc('5c5f69'), hexc('41444c')
SHADE = hexc('1a1b21', 95)
LIGHT = hexc('9ea3b0', 70)
BAND = hexc('27282f')
SOCKET = hexc('0b0b0e')
IRIS = hexc('e2522f')
IRIS_D = hexc('9a2716')
CORE = hexc('f7c94c')
WHITE = hexc('fbfbf6')
CHEST = hexc('25262c')
BODY_T, BODY_B = hexc('6b6e77'), hexc('50535b')
SCARF_T, SCARF_B = hexc('6c6f79'), hexc('4c4f58')
G = hexc('3cf0a0')
G2 = hexc('8dffd4')
TQ = hexc('27d9c4')
GD = hexc('0f5f4a')
PURP = hexc('24172e')

HEAD = [(1500, 560), (1770, 600), (1975, 725), (2130, 905), (2195, 1125), (2155, 1360), (2040, 1545),
        (1860, 1665), (1500, 1715), (1140, 1665), (960, 1545), (845, 1360), (805, 1125), (870, 905),
        (1025, 725), (1230, 600)]
SOCK_L = [(1075, 1195), (1120, 1095), (1250, 1055), (1385, 1100), (1440, 1205), (1385, 1300), (1250, 1330), (1125, 1290)]
SOCK_R = mirror(SOCK_L, CX)
IRIS_L = (1290, 1198)


def M(pts):
    return mirror(pts, CX)


def bumpy(cx, cy, rx, ry, k, amp, n=160, phase=0):
    return [(cx + (rx + amp * math.sin(k * a + phase)) * math.cos(a), cy + (ry + amp * 0.6 * math.sin(k * a + phase)) * math.sin(a))
            for a in (2 * math.pi * i / n for i in range(n))]


def build_parts():
    P = []
    add = P.append

    # 00 guide -------------------------------------------------------------
    g = Part('Guide_Centerline_Pivots', '00_GUIDE', visible=False, note='rig guide: center line + pivots, hidden')
    g.stroke([(CX, 150), (CX, 3300)], hexc('ff3a7a', 160), 5, smooth=False)
    for (x, y) in [(CX, 1715), (CX, 2100), (1250, 1860), (1750, 1860), (1370, 2350), (1630, 2350)]:
        g.stroke(ellipse_pts(x, y, 26, 26), hexc('ff3a7a', 200), 6, closed=True)
    add(g)

    # 01 back fx (fight) -----------------------------------------------------
    p = Part('Fight_Aura_Back', '01_BACK_FX', blend='add', visible=False, toggle='mode:fight', physics='aura pulse',
             param='Param_Fight / Param_AuraPulse', note='local green aura, not full-body white')
    p.glow(bumpy(CX, 1500, 900, 1150, 7, 70), hexc('1c8f68', 150), 90)
    p.glow(bumpy(CX, 1250, 760, 720, 9, 60, phase=1), hexc('2ad49a', 90), 60)
    add(p)
    p = Part('Fight_Ring_Back', '01_BACK_FX', blend='add', visible=False, toggle='mode:fight',
             param='Param_AuraPulse', note='broken spectral ring behind head')
    for a0 in (200, 260, 330, 30, 95):
        p.stroke(arc_pts(CX, 1180, 880, 820, a0, a0 + 42), G, 26, clip=False)
    p.post_blur = 3
    add(p)
    for i, (x, y, s) in enumerate([(820, 520, 1.0), (2210, 700, 0.85)], 1):
        p = Part(f'Shadow_Wisp_0{i}', '01_BACK_FX', visible=False, toggle='mode:fight', physics='wisp float',
                 param=f'Param_Wisp{i}', note='living-shadow wisp')
        path = [(x, y + 260 * s), (x - 60 * s, y + 120 * s), (x + 10 * s, y), (x + 90 * s, y - 90 * s)]
        p.fill(band(path, 150 * s, 18 * s), ('v', PURP, hexc('1b1c22'), y - 100, y + 260), outline=G, ow=7)
        add(p)
    # (derived silhouette echo created in derived())

    # 02 lower shadow -------------------------------------------------------------
    p = Part('Ground_Shadow', '02_LOWER_SHADOW', blend='multiply', param='Param_BodyX (follow)', note='contact shadow')
    p.glow(ellipse_pts(CX, 2880, 470, 62), hexc('5a5c68', 255), 14)
    add(p)
    p = Part('Ground_Shadow_Fight', '02_LOWER_SHADOW', visible=False, toggle='mode:fight', param='Param_Fight',
             note='enlarged living shadow pool')
    p.fill(bumpy(CX + 60, 2885, 760, 95, 11, 22), ('v', hexc('0d0d12', 235), hexc('24172e', 200), 2800, 2980))
    p.stroke(bumpy(CX + 60, 2885, 760, 95, 11, 22), G, 6, closed=True)
    add(p)
    tail = [(1600, 2860), (1760, 2885), (1900, 2845), (2040, 2895), (2180, 2855), (2320, 2890), (2420, 2860)]
    p = Part('Shadow_Tail_Tip', '02_LOWER_SHADOW', physics='tail wave 2', param='Param_Tail2', restore='overlap under tail base')
    p.fill(band(tail[2:], 24, 6), LINE)
    add(p)
    p = Part('Shadow_Tail_Base', '02_LOWER_SHADOW', physics='tail wave 1', param='Param_Tail1', note='lower shadow tail root')
    p.fill(band(tail[:4], 34, 22), LINE)
    add(p)
    p = Part('Tail_Flame_Fight', '02_LOWER_SHADOW', blend='add', visible=False, toggle='mode:fight', physics='flame flicker',
             param='Param_Fight')
    p.glow(band([(2420, 2860), (2440, 2780), (2400, 2690), (2450, 2610)], 90, 10), G, 6)
    p.glow(band([(2420, 2860), (2435, 2790), (2410, 2720)], 40, 6), G2, 3)
    add(p)

    # 03 body --------------------------------------------------------------------
    for side, f in (('L', lambda q: q), ('R', M)):
        leg = f([(1300, 2300), (1480, 2300), (1470, 2600), (1455, 2830), (1305, 2835), (1290, 2600)])
        p = Part(f'Leg_{side}', '03_BODY', param=f'Param_Leg{side}', restore='leg top hidden under lower body')
        p.fill(leg, ('v', BODY_T, BODY_B, 2300, 2840), outline=LINE, ow=9)
        p.shade(shift(leg, 40 if side == 'L' else -40), SHADE, blur=6)
        add(p)
        foot = f(ellipse_pts(1385, 2835, 118, 50))
        p = Part(f'Foot_{side}', '03_BODY', param=f'Param_Leg{side}')
        p.fill(foot, hexc('45474f'), outline=LINE, ow=9)
        p.shade(shift(foot, 30, 30), SHADE)
        p.stroke(f(arc_pts(1385, 2835, 80, 30, 200, 250, 16)), hexc('6a6d77'), 7, clip=True)  # inner toe highlight
        add(p)
    low = [(1245, 2060), (1755, 2060), (1795, 2240), (1745, 2420), (1500, 2455), (1255, 2420), (1205, 2240)]
    p = Part('Body_Lower', '03_BODY', param='Param_BodyAngleX/Y', restore='belly top under chest band')
    p.fill(low, ('v', BODY_T, BODY_B, 2060, 2455), outline=LINE, ow=10)
    p.shade([(1640, 2060), (1800, 2100), (1800, 2460), (1600, 2460)], SHADE, blur=10)
    p.shade(ellipse_pts(1440, 2240, 90, 60), LIGHT, blur=20)
    add(p)
    chest = [(1235, 1770), (1765, 1770), (1810, 1950), (1770, 2130), (1500, 2170), (1230, 2130), (1190, 1950)]
    p = Part('Body_Chest', '03_BODY', param='Param_BodyAngleX/Y, Param_Breath', restore='chest top under scarf')
    p.fill(chest, CHEST, outline=LINE, ow=10)
    p.shade([(1600, 1770), (1820, 1800), (1820, 2180), (1560, 2180)], hexc('0d0d10', 90), blur=12)
    add(p)
    p = Part('Body_Chest_Rim', '03_BODY', blend='screen', param='Param_Breath', note='soft rim light')
    p.stroke(arc_pts(1500, 1960, 290, 190, 200, 250), hexc('565a66'), 16, blur=4)
    add(p)

    # 04 arms ----------------------------------------------------------------------
    for side, f in (('L', lambda q: q), ('R', M)):
        up = f([(1265, 1845), (1175, 1960), (1120, 2060)])
        p = Part(f'Arm_{side}_Upper', '04_ARMS', physics='arm sway', param=f'Param_Arm{side}A',
                 restore='shoulder hidden under chest/scarf')
        p.fill(band(up, 150, 128), CHEST, outline=LINE, ow=9)
        add(p)
        fo = f([(1128, 2045), (1090, 2130), (1070, 2190)])
        p = Part(f'Arm_{side}_Fore', '04_ARMS', physics='arm sway 2', param=f'Param_Arm{side}B', restore='elbow overlap; wrist continues under hand')
        p.fill(band(fo, 128, 120), ('v', hexc('2e2f36'), hexc('3c3e46'), 2040, 2200), outline=LINE, ow=9)
        add(p)
        hand = f([(990, 2190), (1040, 2150), (1120, 2160), (1160, 2215), (1150, 2285), (1125, 2325), (1095, 2300),
                  (1075, 2335), (1045, 2305), (1015, 2330), (995, 2290), (975, 2250)])
        p = Part(f'Hand_{side}', '04_ARMS', param=f'Param_Hand{side}')
        p.fill(hand, hexc('6d707a'), outline=LINE, ow=9)
        p.shade(shift(hand, 25 if side == 'L' else -25, 18), SHADE)
        add(p)
        fist = f(ellipse_pts(1070, 2240, 100, 92))
        p = Part(f'Hand_{side}_Fist', '04_ARMS', visible=False, toggle='mode:fight|pose:fist', param=f'Param_Hand{side}Fist',
                 note='clenched fist swap for fighting stance')
        p.fill(fist, hexc('70737d'), outline=LINE, ow=10)
        for k in range(3):
            p.stroke(f(arc_pts(1030 + k * 42, 2200, 22, 18, 180, 360, 12)), LINE, 6, clip=True)
        p.shade(shift(fist, 0, 45), SHADE)
        add(p)
    # attack pose arm (R raised, palm out) -- reference: palm thrust
    p = Part('Arm_R_Attack', '04_ARMS', visible=False, toggle='pose:attack', param='Param_ArmRAttack',
             note='alt raised arm for attack pose (swap with Arm_R_*)')
    p.fill(band([(1735, 1850), (1860, 1760), (1980, 1690)], 140, 120), CHEST, outline=LINE, ow=9)
    add(p)
    p = Part('Hand_R_Palm_Attack', '04_ARMS', visible=False, toggle='pose:attack', param='Param_ArmRAttack')
    palm = [(1960, 1640), (2010, 1560), (2060, 1580), (2080, 1520), (2130, 1540), (2135, 1600), (2185, 1590),
            (2195, 1660), (2150, 1740), (2060, 1770), (1990, 1740)]
    p.fill(palm, hexc('6d707a'), outline=LINE, ow=9)
    add(p)

    # 05 scarf ---------------------------------------------------------------------
    sc = bumpy(CX, 1760, 425, 140, 9, 34)
    p = Part('Scarf_Main', '05_SCARF', physics='scarf bounce', param='Param_Scarf', restore='covers chin, full ring drawn')
    p.fill(sc, ('v', SCARF_T, SCARF_B, 1620, 1900), outline=LINE, ow=10)
    p.shade(bumpy(CX, 1810, 425, 110, 9, 34), hexc('2e3037', 110), blur=6)
    p.stroke(arc_pts(1500, 1740, 300, 60, 200, 340), hexc('82858f'), 10, clip=True, blur=2)
    add(p)
    for side, f in (('L', lambda q: q), ('R', M)):
        p = Part(f'Scarf_Tuft_{side}', '05_SCARF', physics='scarf tuft', param=f'Param_ScarfTuft{side}')
        tuft = f([(1130, 1760), (1040, 1740), (975, 1790), (1000, 1850), (1080, 1860), (1150, 1830)])
        p.fill(tuft, ('v', SCARF_T, SCARF_B, 1730, 1870), outline=LINE, ow=9)
        add(p)
    p = Part('Scarf_Trail', '05_SCARF', physics='scarf trail (long)', param='Param_ScarfTrail', note='misty trailing end')
    p.fill(band([(1880, 1760), (2000, 1715), (2110, 1760), (2200, 1700), (2260, 1730)], 120, 16),
           ('v', SCARF_T, SCARF_B, 1680, 1800), outline=LINE, ow=8)
    add(p)

    # 06 head ---------------------------------------------------------------------
    crest = [(1500, 700), (1465, 520), (1500, 380), (1590, 300), (1700, 305), (1740, 375), (1690, 425)]
    p = Part('Crest_Tip', '06_HEAD', physics='crest sway 2', param='Param_Crest2', restore='curl root continues under crest base')
    p.fill(band(crest[2:], 140, 40), ('v', HEAD_T, HEAD_B, 280, 440), outline=LINE, ow=10)
    add(p)
    p = Part('Crest_Base', '06_HEAD', physics='crest sway 1', param='Param_Crest1', restore='root hidden inside head')
    p.fill(band(crest[:4], 250, 120), ('v', HEAD_T, HEAD_B, 300, 700), outline=LINE, ow=10)
    p.shade(band(shift(crest[:4], 45, 0), 150, 60), SHADE, blur=6)
    add(p)
    for side, f in (('L', lambda q: q), ('R', M)):
        p = Part(f'Lobe_Tip_{side}', '06_HEAD', physics='tip flick', param=f'Param_LobeTip{side}', restore='tip root under lobe')
        p.fill(f(band([(790, 720), (725, 625), (745, 540), (810, 510)], 90, 18)), ('v', HEAD_T, HEAD_B, 500, 740), outline=LINE, ow=9)
        add(p)
        lobe = f([(690, 965), (685, 820), (760, 700), (885, 648), (1010, 680), (1090, 775), (1100, 905), (1030, 1020), (905, 1065), (785, 1045)])
        p = Part(f'Head_Lobe_{side}', '06_HEAD', physics='lobe bounce', param=f'Param_Lobe{side}',
                 restore='lobe base continues under head')
        p.fill(lobe, ('v', HEAD_T, HEAD_B, 640, 1070), outline=LINE, ow=10)
        p.shade(shift(lobe, 0, 60), SHADE, blur=6)
        add(p)
        sp = [(900 + (160 - 12 * t) * math.cos(t * 0.55) * 0.9, 865 + (160 - 12 * t) * math.sin(t * 0.55) * 0.9) for t in range(0, 12)]
        p = Part(f'Lobe_Swirl_{side}', '06_HEAD', param=f'Param_Lobe{side}', note='swirl line')
        p.stroke(f(sp[::-1]), hexc('24252b'), 16)
        p.stroke(f(shift(sp[::-1][2:], -6, -8)), hexc('777b86'), 6)
        add(p)
    p = Part('Head_Base', '06_HEAD', param='Param_AngleX/Y/Z', restore='chin continues under scarf; crown under crest')
    p.fill(HEAD, ('v', HEAD_T, HEAD_B, 560, 1715), outline=LINE, ow=12)
    p.shade([(1500, 1560), (1950, 1470), (2200, 1300), (2200, 1720), (800, 1720), (800, 1300), (1050, 1470)], SHADE, blur=14)
    p.shade(ellipse_pts(1320, 760, 230, 110, -15), LIGHT, blur=30)
    add(p)
    p = Part('Head_Rim_Light', '06_HEAD', blend='screen', param='Param_AngleX', note='screen rim light')
    p.stroke(arc_pts(1500, 1135, 640, 520, 195, 250), hexc('4a4e5a'), 22, blur=6)
    add(p)

    # 07 face ----------------------------------------------------------------------
    bandpts = [(700, 1070), (1100, 1030), (1500, 1095), (1900, 1030), (2300, 1070), (2300, 1345), (1900, 1375),
               (1500, 1320), (1100, 1375), (700, 1345)]
    p = Part('Face_EyeBand', '07_FACE', param='Param_AngleX/Y', note='dark mask band (clipped to head)')
    p.fill(bandpts, BAND)
    p.clip(HEAD)
    add(p)
    p = Part('Face_Band_Edge', '07_FACE', param='Param_AngleX/Y', note='band soft top edge')
    p.stroke(bandpts[:5], hexc('34363e'), 14, blur=3)
    p.clip(HEAD)
    add(p)

    # 08 eyes ------------------------------------------------------------------------
    for side, f in (('L', lambda q: q), ('R', M)):
        s = 1 if side == 'L' else -1
        ix = IRIS_L[0] if side == 'L' else 2 * CX - IRIS_L[0]
        iy = IRIS_L[1]
        sock = SOCK_L if side == 'L' else SOCK_R
        p = Part(f'Eye{side}_Socket', '08_EYES', param=f'Param_EyeOpen{side}', restore='full socket under lids')
        p.fill(sock, SOCKET, outline=hexc('3b3d46'), ow=6)
        add(p)
        p = Part(f'Eye{side}_Iris', '08_EYES', param='Param_EyeBallX/Y', restore='full oval under socket clip')
        p.fill(ellipse_pts(ix, iy, 72, 104), ('r', hexc('f06a3a'), IRIS_D, ix - 18, iy - 22, 120), outline=hexc('5a1409'), ow=6)
        p.shade(shift(sock, 0, -150), hexc('2a0a05', 120), blur=8)  # upper-lid cast shadow (follows socket tilt)
        add(p)
        p = Part(f'Eye{side}_Core', '08_EYES', param='Param_EyeBallX/Y')
        p.fill(ellipse_pts(ix + 4 * s, iy - 2, 30, 60), ('r', hexc('fff3b0'), CORE, ix, iy, 60))
        add(p)
        p = Part(f'Eye{side}_Highlight01', '08_EYES', param='Param_EyeBallX/Y (0.5)')
        p.fill(ellipse_pts(ix - 26, iy - 58, 20 + 3 * s, 16), WHITE)
        add(p)
        p = Part(f'Eye{side}_Highlight02', '08_EYES', param='Param_EyeBallX/Y (0.5)')
        p.fill(ellipse_pts(ix + 26, iy + 62, 10, 8 + s), hexc('ffffff', 220))
        add(p)
        p = Part(f'Eye{side}_Iris_Fight', '08_EYES', visible=False, toggle='mode:fight', param='Param_Fight',
                 note='spectral green iris swap')
        p.fill(ellipse_pts(ix, iy, 74, 106), ('r', hexc('d8fff0'), hexc('0ea57a'), ix, iy, 112), outline=GD, ow=6)
        p.fill(ellipse_pts(ix + 4 * s, iy - 2, 24, 58), hexc('f4fffb'))
        add(p)
        p = Part(f'Eye{side}_Iris_Small', '08_EYES', visible=False, toggle='eye:small', param='Param_EyeSurprise',
                 note='shrunken iris (surprise)')
        p.fill(ellipse_pts(ix, iy, 40, 58), ('r', hexc('f06a3a'), IRIS_D, ix - 10, iy - 12, 66))
        p.shade(shift(sock, 0, -170), hexc('2a0a05', 120), blur=6)
        p.fill(ellipse_pts(ix - 14, iy - 30, 9, 7), WHITE)
        p.fill(ellipse_pts(ix, iy, 14, 26), CORE)
        add(p)
        p = Part(f'Eye{side}_UpperLid', '08_EYES', param=f'Param_EyeOpen{side}', note='upper lid rim for blink deform')
        p.stroke(f([(1085, 1180), (1125, 1098), (1250, 1058), (1382, 1100), (1432, 1195)]), hexc('4a4d57'), 12)
        add(p)
        p = Part(f'Eye{side}_LowerLid', '08_EYES', param=f'Param_EyeOpen{side}')
        p.stroke(f([(1135, 1292), (1250, 1325), (1380, 1298)]), hexc('3d3f48'), 8)
        add(p)
        p = Part(f'Eye{side}_Closed', '08_EYES', visible=False, toggle='eye:closed', param=f'Param_EyeOpen{side}=0',
                 note='closed eye line')
        p.stroke(f([(1090, 1225), (1170, 1255), (1260, 1262), (1350, 1245), (1430, 1215)]), hexc('8d919c'), 13)
        add(p)
        p = Part(f'Eye{side}_Happy', '08_EYES', visible=False, toggle='eye:happy', param=f'Param_EyeSmile{side}',
                 note='^ smile-closed eye')
        p.stroke(f([(1110, 1265), (1180, 1190), (1260, 1165), (1340, 1190), (1410, 1265)]), hexc('a3a7b2'), 16)
        add(p)
        p = Part(f'Eye{side}_Lid_Angry', '08_EYES', visible=False, toggle='lid:angry', param=f'Param_EyeForm{side}',
                 note='band-coloured lid cutting inner-top of socket')
        p.fill(f([(1060, 1030), (1470, 1030), (1470, 1240), (1300, 1150), (1060, 1075)]), BAND, smooth=False)
        p.stroke(f([(1090, 1090), (1300, 1155), (1450, 1230)]), hexc('4a4d57'), 12, smooth=False)
        p.clip(bandpts, smooth=True)
        add(p)
        p = Part(f'Eye{side}_Lid_Sad', '08_EYES', visible=False, toggle='lid:sad', param=f'Param_EyeForm{side}',
                 note='band-coloured lid cutting outer-top of socket')
        p.fill(f([(1050, 1030), (1460, 1030), (1460, 1085), (1260, 1115), (1050, 1230)]), BAND, smooth=False)
        p.stroke(f([(1070, 1210), (1250, 1122), (1430, 1098)]), hexc('4a4d57'), 12, smooth=False)
        p.clip(bandpts, smooth=True)
        add(p)
        p = Part(f'Eye{side}_Rage_Mark', '08_EYES', visible=False, toggle='mode:fight', param='Param_Fight',
                 note='jagged spectral mark above eye (fighting)')
        jag = f([(1200, 1010), (1250, 925), (1235, 985), (1300, 900), (1285, 975), (1345, 930), (1300, 1030)])
        p.fill(jag, G2, smooth=False, outline=GD, ow=6)
        add(p)

    # 09 marks ------------------------------------------------------------------------
    for side, f in (('L', lambda q: q), ('R', M)):
        p = Part(f'Blush_{side}', '09_MARKS', visible=False, toggle='fx:blush', param='Param_Cheek')
        for k in range(3):
            p.stroke(f([(1060 + k * 45, 1440), (1085 + k * 45, 1395)]), hexc('ff8fb0', 230), 10, smooth=False)
        add(p)
        p = Part(f'Tear_{side}', '09_MARKS', visible=False, toggle='fx:tear', physics='tear drip', param='Param_Tear')
        tx = 1150 if side == 'L' else 1850
        p.fill([(tx, 1320), (tx + 28, 1410), (tx + 22, 1470), (tx, 1490), (tx - 22, 1470), (tx - 28, 1410)],
               ('v', hexc('bfeaff', 240), hexc('59b8ff', 240), 1320, 1490), outline=hexc('2a6fb0'), ow=5)
        p.fill(f(ellipse_pts(1140, 1440, 7, 14)), WHITE)
        add(p)
    p = Part('Mark_Anger_Vein', '09_MARKS', visible=False, toggle='fx:anger', param='Param_Anger')
    for a in (0, 90, 180, 270):
        c, s_ = math.cos(math.radians(a + 45)), math.sin(math.radians(a + 45))
        p.stroke([(1900 + 30 * c, 820 + 30 * s_), (1900 + 70 * c + 25 * s_, 820 + 70 * s_ - 25 * c),
                  (1900 + 75 * c, 820 + 75 * s_)], hexc('ff5a4e'), 16)
    add(p)
    p = Part('Mark_Sweat', '09_MARKS', visible=False, toggle='fx:sweat', param='Param_Sweat')
    p.fill([(2080, 900), (2115, 990), (2105, 1040), (2080, 1055), (2055, 1040), (2045, 990)], hexc('9edcff', 235),
           outline=hexc('2a6fb0'), ow=5)
    add(p)
    p = Part('Mark_Zzz', '09_MARKS', visible=False, toggle='fx:sleep', param='Param_Sleep')
    for i, (x, y, s_) in enumerate([(1980, 760, 60), (2080, 650, 80), (2200, 520, 100)]):
        p.stroke([(x, y), (x + s_, y), (x, y + s_), (x + s_, y + s_)], hexc('c8f5ff'), 12 + i * 2, smooth=False)
    add(p)
    p = Part('Mark_Confused', '09_MARKS', visible=False, toggle='fx:confused', param='Param_Confused')
    sp = [(1950 + (8 * t) * math.cos(t * 0.6), 820 + (8 * t) * math.sin(t * 0.6)) for t in range(3, 14)]
    p.stroke(sp, hexc('d0d4ff'), 12)
    p.stroke([(2100, 700), (2110, 640), (2150, 610), (2190, 640), (2170, 690), (2140, 720), (2140, 760)], hexc('d0d4ff'), 14)
    p.fill(ellipse_pts(2140, 800, 12, 12), hexc('d0d4ff'))
    add(p)
    p = Part('Mark_Surprise', '09_MARKS', visible=False, toggle='fx:surprise', param='Param_Surprise')
    for a in (-60, -35, -10):
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        p.stroke([(1500 + 720 * c, 1100 + 650 * s_), (1500 + 820 * c, 1100 + 740 * s_)], hexc('f2f2f2'), 14, smooth=False)
        p.stroke([(1500 - 720 * c, 1100 + 650 * s_), (1500 - 820 * c, 1100 + 740 * s_)], hexc('f2f2f2'), 14, smooth=False)
    add(p)
    p = Part('Mark_Sparkle', '09_MARKS', visible=False, toggle='fx:sparkle', param='Param_Happy')
    for (x, y, r) in [(2120, 820, 60), (880, 1450, 40), (2050, 1480, 34)]:
        p.fill([(x, y - r), (x + r * .25, y - r * .25), (x + r, y), (x + r * .25, y + r * .25), (x, y + r), (x - r * .25, y + r * .25),
                (x - r, y), (x - r * .25, y - r * .25)], hexc('fff7c2'), smooth=False)
    add(p)

    # 10 mouth ------------------------------------------------------------------------
    MX, MY = 1500, 1478
    p = Part('Mouth_Neutral', '10_MOUTH', toggle='mouth:neutral', param='Param_MouthForm', note='default small frown')
    p.stroke([(MX - 48, MY + 10), (MX, MY - 12), (MX + 48, MY + 10)], LINE, 10)
    add(p)
    p = Part('Mouth_Smile', '10_MOUTH', visible=False, toggle='mouth:smile', param='Param_MouthForm=+1')
    p.stroke([(MX - 55, MY - 12), (MX, MY + 14), (MX + 55, MY - 12)], LINE, 10)
    add(p)
    open_pts = [(MX - 70, MY - 20), (MX, MY - 8), (MX + 70, MY - 20), (MX + 45, MY + 45), (MX, MY + 62), (MX - 45, MY + 45)]
    p = Part('Mouth_Open_Inner', '10_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthOpenY')
    p.fill(open_pts, hexc('2b0e14'))
    add(p)
    p = Part('Mouth_Open_Tongue', '10_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthOpenY')
    p.fill(ellipse_pts(MX, MY + 44, 38, 20), hexc('e0707a'))
    p.clip(open_pts)
    add(p)
    p = Part('Mouth_Open_Line', '10_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthOpenY/Form')
    p.stroke(open_pts, LINE, 9, closed=True)
    add(p)
    grit = [(MX - 75, MY - 15), (MX + 75, MY - 15), (MX + 65, MY + 30), (MX - 65, MY + 30)]
    p = Part('Mouth_Grit_Teeth', '10_MOUTH', visible=False, toggle='mouth:grit', param='Param_MouthForm=-1',
             note='clenched fighting teeth')
    p.fill(grit, WHITE, smooth=False)
    for k in (-35, 0, 35):
        p.stroke([(MX + k, MY - 15), (MX + k, MY + 30)], hexc('7a7d88'), 5, smooth=False)
    p.stroke([(MX - 70, MY + 8), (MX + 70, MY + 8)], hexc('7a7d88'), 4, smooth=False)
    p.stroke(grit, LINE, 9, closed=True, smooth=False)
    add(p)
    p = Part('Mouth_Sad', '10_MOUTH', visible=False, toggle='mouth:sad', param='Param_MouthForm=-1')
    p.stroke([(MX - 55, MY + 20), (MX, MY - 16), (MX + 55, MY + 20)], LINE, 10)
    add(p)
    p = Part('Mouth_Smirk', '10_MOUTH', visible=False, toggle='mouth:smirk', param='Param_MouthForm (asym)')
    p.stroke([(MX - 50, MY + 6), (MX + 10, MY + 6), (MX + 60, MY - 22)], LINE, 10)
    add(p)
    p = Part('Mouth_O', '10_MOUTH', visible=False, toggle='mouth:o', param='Param_MouthOpenY')
    p.fill(ellipse_pts(MX, MY + 10, 30, 38), hexc('2b0e14'), outline=LINE, ow=9)
    add(p)
    p = Part('Mouth_Wavy', '10_MOUTH', visible=False, toggle='mouth:wavy', param='Param_MouthForm')
    p.stroke([(MX - 70 + 20 * k, MY + (10 if k % 2 else -8)) for k in range(8)], LINE, 9)
    add(p)
    p = Part('Mouth_Fang', '10_MOUTH', visible=False, toggle='mouth:fang', param='Param_MouthOpenY')
    p.fill([(MX + 22, MY - 14), (MX + 50, MY - 18), (MX + 38, MY + 16)], WHITE, smooth=False)
    add(p)

    # 11 front fx -----------------------------------------------------------------------
    p = Part('Crest_Flame_Fight', '11_FRONT_FX', blend='add', visible=False, toggle='mode:fight', physics='flame flicker',
             param='Param_Fight / Param_Flame')
    fl = [(1500, 640), (1440, 470), (1470, 300), (1560, 170), (1660, 120), (1620, 220), (1720, 190), (1690, 320),
          (1610, 430), (1570, 640)]
    p.glow(fl, ('v', hexc('b5ffe0'), hexc('1fae7f'), 120, 640), 10)
    p.glow(scale(fl, 0.55, 0.7, 1530, 640), G2, 8)
    add(p)
    for side, f in (('L', lambda q: q), ('R', M)):
        p = Part(f'Lobe_Flame_{side}', '11_FRONT_FX', blend='add', visible=False, toggle='mode:fight', physics='flame flicker',
                 param='Param_Fight')
        p.glow(f([(760, 720), (680, 600), (660, 470), (730, 380), (740, 480), (800, 430), (830, 560), (860, 680)]),
               ('v', hexc('a8ffd9'), hexc('1a9e73'), 380, 720), 9)
        add(p)
        p = Part(f'Eye{side}_Glow', '11_FRONT_FX', blend='add', visible=False, toggle='mode:fight|fx:eyeglow',
                 param='Param_EyeGlow')
        ix = IRIS_L[0] if side == 'L' else 2 * CX - IRIS_L[0]
        p.glow(f(scale(SOCK_L, 1.15, 1.25, 1260, 1195)), hexc('23c98f', 190), 40)
        add(p)
    p = Part('Particles_01', '11_FRONT_FX', blend='add', visible=False, toggle='mode:fight', physics='float up',
             param='Param_Particles')
    rng = np.random.default_rng(7)
    for _ in range(26):
        x, y = rng.uniform(650, 2350), rng.uniform(300, 1500)
        if abs(x - CX) < 700 and 550 < y < 1720:
            continue
        r = rng.uniform(8, 20)
        p.glow(ellipse_pts(x, y, r, r), G2, 3)
    add(p)
    p = Part('Particles_02', '11_FRONT_FX', blend='add', visible=False, toggle='mode:fight', physics='float up (offset)',
             param='Param_Particles')
    for _ in range(22):
        x, y = rng.uniform(650, 2400), rng.uniform(1700, 2900)
        if abs(x - CX) < 380:
            continue
        s_ = rng.uniform(14, 30)
        p.glow([(x, y - s_), (x + s_ * .4, y), (x, y + s_), (x - s_ * .4, y)], TQ, 2, smooth=False)
    add(p)

    # 12 combat -------------------------------------------------------------------------
    for side, f in (('L', lambda q: q), ('R', M)):
        p = Part(f'Arm_{side}_Energy', '12_COMBAT', blend='add', visible=False, toggle='mode:fight|fx:combathands',
                 physics='swirl', param='Param_CombatHands')
        cxh, cyh = (1070 if side == 'L' else 1930), 2150
        for k in range(3):
            p.stroke(arc_pts(cxh, cyh - 60 + k * 70, 150, 42, 200 + k * 20, 470 + k * 20), G, 12, blur=2)
        p.glow(ellipse_pts(cxh, 2240, 150, 150), hexc('1a8f66', 150), 30)
        add(p)
        p = Part(f'Shadow_Hand_{side}', '12_COMBAT', visible=False, toggle='mode:fight|fx:combathands',
                 physics='float + follow hand', param=f'Param_ShadowHand{side}', note='big living-shadow hand')
        hx, hy = (700 if side == 'L' else 2300), 1980
        sh = [(hx - 170, hy + 60), (hx - 150, hy - 110), (hx - 95, hy - 150), (hx - 60, hy - 70), (hx - 40, hy - 250),
              (hx + 10, hy - 265), (hx + 30, hy - 100), (hx + 70, hy - 270), (hx + 120, hy - 250), (hx + 110, hy - 90),
              (hx + 170, hy - 200), (hx + 215, hy - 170), (hx + 170, hy + 40), (hx + 90, hy + 180), (hx - 60, hy + 200)]
        sh = f(mirror(sh, hx)) if side == 'L' else sh
        if side == 'R':
            sh = sh
        p.fill(sh, ('v', hexc('15121c', 230), hexc('2a1a38', 200), hy - 270, hy + 200), outline=G, ow=8)
        p.shade(shift(sh, 0, 60), hexc('000000', 80), blur=10)
        add(p)
        p = Part(f'Shadow_Hand_{side}_Glow', '12_COMBAT', blend='add', visible=False, toggle='mode:fight|fx:combathands',
                 param=f'Param_ShadowHand{side}')
        p.glow(sh, hexc('1b9c70', 170), 36)
        add(p)
    p = Part('Fight_Aura_Pulse', '12_COMBAT', blend='add', visible=False, toggle='mode:rage', param='Param_AuraPulse',
             note='shadow rage pulse ring (local)')
    p.stroke(bumpy(CX, 1650, 980, 1180, 12, 40), hexc('32e6a0', 200), 22, closed=True, blur=6)
    add(p)
    p = Part('Rage_Mist', '12_COMBAT', visible=False, toggle='mode:rage', param='Param_Rage', note='dark mist around feet')
    p.glow(bumpy(CX, 2820, 820, 190, 9, 50), hexc('140f1c', 170), 30)
    add(p)
    return P


def derived(recs, W, H):
    """silhouette-derived fight layers: green outline glow + mimicry shadow echo."""
    from partkit import blend_over
    body_groups = {'03_BODY', '04_ARMS', '05_SCARF', '06_HEAD'}
    k = 4
    a = np.zeros((H // k, W // k), np.float32)
    for r in recs:
        if r['group'] in body_groups and r['visible'] and r['blend'] == 'normal':
            al = r['img'].getchannel('A').resize((max(1, r['img'].width // k), max(1, r['img'].height // k)), Image.BOX)
            arr = np.asarray(al, np.float32) / 255
            y, x = r['y'] // k, r['x'] // k
            sub = a[y:y + arr.shape[0], x:x + arr.shape[1]]
            sub[:] = np.maximum(sub, arr[:sub.shape[0], :sub.shape[1]])
    sil = Image.fromarray((a * 255).astype(np.uint8))
    dil = sil.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(6))
    ring = ImageChops.subtract(dil, sil.filter(ImageFilter.GaussianBlur(1)))
    ring = ring.resize((W, H), Image.BILINEAR)
    glow = Image.new('RGBA', (W, H), G)
    glow.putalpha(ring)
    bb = ring.point(lambda v: 255 if v > 3 else 0).getbbox()
    out = []
    p = Part('Outline_Glow_Fight', '11_FRONT_FX', blend='add', visible=False, toggle='mode:fight', param='Param_Fight',
             note='silhouette-derived spectral outline')
    out.append((p, glow.crop(bb), bb[0], bb[1]))
    echo = Image.new('RGBA', (W, H), PURP)
    ea = sil.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR).point(lambda v: int(v * 0.72))
    echo.putalpha(ea)
    echo = ImageChops.offset(echo, 70, 25)
    bb = echo.getchannel('A').point(lambda v: 255 if v > 3 else 0).getbbox()
    p = Part('Shadow_Clone_Echo', '01_BACK_FX', visible=False, toggle='mode:fight', physics='lag follow (mimicry)',
             param='Param_Fight / Param_EchoX', note='living-shadow mimic echo')
    out.append((p, echo.crop(bb), bb[0], bb[1]))
    return out


# ---------------------------------------------------------------------- states
FIGHT = ['mode:fight']
EXPR = {
    'Neutral': {},
    'Happy': {'on': ['mouth:smile', 'fx:blush'], 'off': ['mouth:neutral']},
    'Big_Smile': {'on': ['eye:happy', 'mouth:open', 'fx:blush', 'fx:sparkle'],
                  'off': ['mouth:neutral', 'EyeL_Socket', 'EyeR_Socket', 'EyeL_Iris', 'EyeR_Iris', 'EyeL_Core', 'EyeR_Core',
                          'EyeL_Highlight01', 'EyeR_Highlight01', 'EyeL_Highlight02', 'EyeR_Highlight02',
                          'EyeL_UpperLid', 'EyeR_UpperLid', 'EyeL_LowerLid', 'EyeR_LowerLid']},
    'Mischievous': {'on': ['lid:angry', 'mouth:smirk', 'mouth:fang'], 'off': ['mouth:neutral']},
    'Surprised': {'on': ['eye:small', 'mouth:o', 'fx:surprise', 'fx:sweat'],
                  'off': ['mouth:neutral', 'EyeL_Iris', 'EyeR_Iris', 'EyeL_Core', 'EyeR_Core']},
    'Angry': {'on': ['lid:angry', 'mouth:grit', 'fx:anger'], 'off': ['mouth:neutral']},
    'Sad': {'on': ['lid:sad', 'mouth:sad'], 'off': ['mouth:neutral']},
    'Crying': {'on': ['lid:sad', 'mouth:wavy', 'fx:tear'], 'off': ['mouth:neutral']},
    'Sleepy': {'on': ['eye:closed', 'mouth:o', 'fx:sleep'],
               'off': ['mouth:neutral', 'EyeL_Socket', 'EyeR_Socket', 'EyeL_Iris', 'EyeR_Iris', 'EyeL_Core', 'EyeR_Core',
                       'EyeL_Highlight01', 'EyeR_Highlight01', 'EyeL_Highlight02', 'EyeR_Highlight02',
                       'EyeL_UpperLid', 'EyeR_UpperLid', 'EyeL_LowerLid', 'EyeR_LowerLid']},
    'Confused': {'on': ['mouth:wavy', 'fx:confused', 'EyeR_Lid_Sad'], 'off': ['mouth:neutral']},
    'Fighting': {'on': FIGHT + ['lid:angry', 'mouth:grit', 'pose:fist'], 'off': ['mouth:neutral', 'Hand_L', 'Hand_R']},
    'Shadow_Rage': {'on': FIGHT + ['mode:rage', 'lid:angry', 'mouth:open', 'mouth:fang', 'fx:anger', 'pose:fist'],
                    'off': ['mouth:neutral', 'Hand_L', 'Hand_R']},
}
STATES = {'NORMAL': {}, 'SHADOW_FIGHTING': EXPR['Fighting'], 'SHADOW_RAGE': EXPR['Shadow_Rage'],
          'ATTACK_POSE': {'on': FIGHT + ['pose:attack', 'lid:angry', 'mouth:grit'],
                          'off': ['mouth:neutral', 'Arm_R_Upper', 'Arm_R_Fore', 'Hand_R', 'Hand_R_Fist']}}
for k, v in EXPR.items():
    STATES['EXPR_' + k] = v


def sheets(ctx):
    recs, comps, root = ctx['recs'], ctx['comps'], ctx['root']
    md = os.path.join(root, 'masters')
    os.makedirs(md, exist_ok=True)
    bg = (236, 238, 242, 255)
    ctx['flat'](comps['NORMAL'], bg).save(os.path.join(md, 'MSM_MINI_NORMAL_MASTER_v001.png'))
    ctx['flat'](comps['SHADOW_FIGHTING'], (30, 32, 38, 255)).save(os.path.join(md, 'MSM_MINI_FIGHTING_MASTER_v001.png'))
    face = (650, 150, 2350, 1950)
    tiles = [(k.replace('_', ' '), ctx['composite'](recs, v, W, H, face)) for k, v in EXPR.items()]
    ctx['label_sheet'](tiles, 4, 'MSM MINI — EXPRESSION MASTER (12) — real PSD parts', (24, 26, 32), scale=0.5).save(
        os.path.join(md, 'MSM_MINI_EXPRESSION_MASTER_v001.png'))
    fx = [r for r in recs if r['group'] in ('01_BACK_FX', '11_FRONT_FX', '12_COMBAT') or 'Fight' in r['name']]
    tiles = []
    for r in fx:
        t = Image.new('RGBA', r['img'].size, (0, 0, 0, 0))
        t.alpha_composite(r['img'])
        t.thumbnail((520, 520))
        tiles.append((r['name'][:24], t))
    ctx['label_sheet'](tiles, 6, 'MSM MINI — FX MASTER (isolated FX / combat parts)', (18, 19, 24), tile_bg=(20, 22, 28, 255)).save(
        os.path.join(md, 'MSM_MINI_FX_MASTER_v001.png'))
    # toggle QA
    tq = [('NORMAL', {}), ('SHADOW FIGHTING (F8)', STATES['SHADOW_FIGHTING']), ('SHADOW RAGE (Shift+F8)', STATES['SHADOW_RAGE']),
          ('ATTACK POSE', STATES['ATTACK_POSE']),
          ('Eye Glow only (Ctrl+1)', {'on': ['fx:eyeglow']}), ('Combat Hands only (Ctrl+3)', {'on': ['fx:combathands', 'pose:fist'], 'off': ['Hand_L', 'Hand_R']}),
          ('Happy', EXPR['Happy']), ('Angry', EXPR['Angry']), ('Sad', EXPR['Sad']), ('Mischievous', EXPR['Mischievous'])]
    tiles = [(n, ctx['composite'](recs, s, W, H).resize((W // 4, H // 4), Image.LANCZOS)) for n, s in tq]
    ctx['label_sheet'](tiles, 5, 'Mini_Toggle_QA — rendered from real PSD parts', (24, 26, 32), tile_bg=(210, 214, 222, 255)).save(
        os.path.join(root, 'qa', 'Mini_Toggle_QA.png'))
