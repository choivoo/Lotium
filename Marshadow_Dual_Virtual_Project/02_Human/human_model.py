"""KAGETSU (影月) — human shadow VTuber Live2D model definition.
Original character: hooded urban-ghost techwear fighter, living shadow + broken-crescent spectral halo.
Modes: NORMAL / SHADOW / COMBAT / OVERDRIVE (+ hood up/down). L = viewer's left.
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '03_Shared_Tools'))
from partkit import Part, hexc, ellipse_pts, mirror, band, shift, arc_pts, scale  # noqa

W, H, CX = 3072, 4608, 1536
MODEL = dict(code='MSH', title='KAGETSU — Human Shadow VTuber', W=W, H=H, root=HERE,
             psd='Marshadow_Human_Live2D_Master_v001.psd', default_state='NORMAL',
             face_box=(1280, 560, 1790, 1040), body_box=(1100, 1200, 1980, 2400), min_restore=15,
             groups=['00_GUIDE', '01_BACK_FX', '02_SHADOW_POOL', '03_BACK_HAIR', '04_HOOD_BACK', '05_BODY',
                     '06_CLOTHES', '07_ARMS', '08_FACE', '09_EYES', '10_BROWS', '11_MOUTH', '12_FRONT_HAIR',
                     '13_HOOD_UP', '14_SHADOW', '15_FRONT_FX', '16_EXPRESSIONS', '17_OVERDRIVE'])

# palette ------------------------------------------------------------------
SKIN, SKIN_S, SKIN_L = hexc('f2d8c8'), hexc('d9a898', 150), hexc('b77f73')
HAIR_T, HAIR_B, HAIR_LN = hexc('454852'), hexc('1f2126'), hexc('0f1013')
JK_T, JK_B, JK_LN = hexc('363841'), hexc('23242a'), hexc('0e0e11')
INNER = hexc('2b2d34')
PANTS_T, PANTS_B = hexc('30323a'), hexc('24252b')
SHADE = hexc('0a0a0e', 90)
G, G2, GD, TQ = hexc('3cf0a0'), hexc('a6ffdc'), hexc('0f6b50'), hexc('27d9c4')
PURP, PURP2 = hexc('23162e'), hexc('3d2552')
IRIS_C, IRIS_E = hexc('5d7f86'), hexc('1c2a30')
WHITE = hexc('fbfbf8')
LASH = hexc('17151b')

FACE = [(1536, 470), (1690, 500), (1760, 600), (1772, 720), (1762, 820), (1730, 900), (1668, 968), (1592, 1010),
        (1536, 1020), (1480, 1010), (1404, 968), (1342, 900), (1310, 820), (1300, 720), (1312, 600), (1382, 500)]
SCL_L = [(1374, 806), (1394, 768), (1440, 752), (1490, 764), (1508, 800), (1486, 836), (1440, 846), (1398, 834)]
EYE_L = (1446, 800)


def M(p):
    return mirror(p, CX)


def ID(p):
    return p


SIDES = (('L', ID, 1), ('R', M, -1))


def jag_bottom(x0, x1, y, n, depth, seed=0):
    rng = np.random.default_rng(seed)
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y + (depth * rng.uniform(0.6, 1.0) if i % 2 else 0)))
    return pts


Y_KNOTS = [(0, 0), (1150, 1150), (1975, 2170), (4340, 4340), (4608, 4608)]


def ymap(y):
    for (a0, b0), (a1, b1) in zip(Y_KNOTS, Y_KNOTS[1:]):
        if y <= a1:
            return b0 + (y - a0) * (b1 - b0) / (a1 - a0)
    return y


def remap(p):
    """piecewise vertical remap below the neck: longer torso / shorter legs (~6.8 heads)."""
    ops = []
    for op in p.ops:
        op = list(op)
        op[1] = [(x, ymap(y)) for x, y in op[1]]
        c = op[2]
        if isinstance(c, tuple) and c and c[0] == 'v':
            c = ('v', c[1], c[2], ymap(c[3]), ymap(c[4]))
        elif isinstance(c, tuple) and c and c[0] == 'r':
            c = ('r', c[1], c[2], c[3], ymap(c[4]), c[5])
        op[2] = c
        ops.append(tuple(op))
    p.ops = ops
    return p


def build_parts():
    P = []
    add = P.append

    # 00 guide --------------------------------------------------------------------
    g = Part('Guide_Centerline_Pivots', '00_GUIDE', visible=False, note='rig guide: centre line, pivots, head/body ratios')
    g.stroke([(CX, 250), (CX, 4450)], hexc('ff3a7a', 150), 5, smooth=False)
    for y in (420, 1020, 1620, 2220, 2820, 3420, 4020):
        g.stroke([(900, y), (2170, y)], hexc('3aa0ff', 110), 3, smooth=False)
    for (x, y) in [(CX, 1010), (CX, 1180), (CX, 1880), (1270, 1210), (1802, 1210), (1440, 2000), (1632, 2000)]:
        g.stroke(ellipse_pts(x, y, 24, 24), hexc('ff3a7a', 200), 6, closed=True)
    add(g)

    # 01 back fx ---------------------------------------------------------------------
    # signature: broken crescent spectral halo
    segs = [(110, 175), (185, 250), (262, 318), (330, 368)]
    p = Part('Halo_Crescent_Main', '01_BACK_FX', visible=False, toggle='mode:shadow|fx:halo', physics='halo float',
             param='Param_Halo / Param_AngleX(0.3)', note='SIGNATURE broken-crescent halo (solid)')
    for a0, a1 in segs:
        outer = arc_pts(CX, 700, 470, 470, a0, a1, 30)
        inner = arc_pts(CX + 60, 660, 400, 400, a1, a0, 30)
        p.fill(outer + inner, ('v', hexc('17151f'), PURP2, 250, 1150), smooth=False, outline=G, ow=7)
    add(p)
    p = Part('Halo_Crescent_Glow', '01_BACK_FX', blend='add', visible=False, toggle='mode:shadow|fx:halo',
             param='Param_HaloGlow')
    for a0, a1 in segs:
        p.glow(arc_pts(CX, 700, 480, 480, a0, a1, 30) + arc_pts(CX + 60, 660, 390, 390, a1, a0, 30), hexc('1fae7f', 170), 24, smooth=False)
    add(p)
    p = Part('Halo_Fragments', '01_BACK_FX', visible=False, toggle='mode:od|fx:halo', physics='drift',
             param='Param_Overdrive', note='broken pieces flying off the crescent (overdrive)')
    for (x, y, r, a) in [(1990, 330, 46, 20), (2080, 440, 30, 70), (1930, 230, 24, 130), (1110, 250, 34, 45)]:
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        p.fill([(x + r * c, y + r * s), (x - r * .4 * s, y + r * .4 * c), (x - r * c, y - r * s), (x + r * .5 * s, y - r * .5 * c)],
               PURP2, smooth=False, outline=G, ow=5)
    add(p)
    for i, (x, y, s) in enumerate([(930, 1250, 1.0), (2150, 1150, 0.9)], 1):
        p = Part(f'Wisp0{i}', '01_BACK_FX', visible=False, toggle='mode:shadow|fx:halo', physics='wisp float / trail',
                 param=f'Param_Wisp{i}', note='floating shadow wisp')
        path = [(x, y + 330 * s), (x - 70 * s, y + 170 * s), (x + 20 * s, y), (x + 120 * s, y - 100 * s), (x + 60 * s, y - 180 * s)]
        wp = band(path, 190 * s, 14 * s)
        p.fill(wp, ('v', hexc('0f0e14'), PURP, y - 180, y + 330), outline=G, ow=6)
        p.fill(ellipse_pts(x - 20 * s, y + 200 * s, 34 * s, 44 * s), G2)
        add(p)
    p = Part('Overdrive_Flame_Back', '01_BACK_FX', blend='add', visible=False, toggle='mode:od', physics='flame flicker',
             param='Param_Overdrive', note='green shadow flame behind body (local)')
    fl = [(1120, 1900), (1040, 1500), (1100, 1150), (1060, 900), (1200, 1000), (1260, 700), (1340, 820), (1420, 560),
          (1536, 700), (1650, 540), (1730, 820), (1820, 680), (1880, 1000), (2010, 880), (1980, 1180), (2040, 1520), (1950, 1900)]
    p.glow(fl, ('v', hexc('9cffd6', 200), hexc('0c6e4f', 60), 560, 1900), 30)
    add(p)
    p = Part('Mist_Back', '01_BACK_FX', visible=False, toggle='mode:od|fx:mist', physics='mist drift', param='Param_Mist')
    rng = np.random.default_rng(3)
    for _ in range(9):
        x, y = rng.uniform(900, 2170), rng.uniform(3500, 4300)
        p.glow(ellipse_pts(x, y, rng.uniform(180, 320), rng.uniform(70, 120)), hexc('1a1422', 150), 40)
    add(p)
    for side, f, s in SIDES:
        arm = f([(1250, 4300), (1000, 3900), (820, 3300), (760, 2800), (720, 2420)])
        p = Part(f'ShadowArm_Rear_{side}', '01_BACK_FX', visible=False, toggle='mode:combat|fx:shadowhands',
                 physics='arm sway (slow)', param=f'Param_ShadowArm{side}', note='shadow arm rising from pool',
                 restore='arm root continues under pool / body')
        p.fill(band(arm, 260, 150), ('v', hexc('0e0c13', 235), hexc('2a1a38', 225), 2400, 4300), outline=G, ow=6)
        p.shade(band(shift(arm, 30 * s, 0), 150, 70), hexc('000000', 90), blur=12)
        add(p)

    # 02 shadow pool --------------------------------------------------------------------
    p = Part('ShadowPool', '02_SHADOW_POOL', param='Param_ShadowPool', note='small calm living shadow (normal)')
    p.fill(ellipse_pts(CX, 4330, 430, 70), ('r', hexc('14111a', 230), hexc('2a1d36', 90), CX, 4330, 430), blur=6)
    add(p)
    p = Part('ShadowPool_Large', '02_SHADOW_POOL', visible=False, toggle='mode:shadow', param='Param_ShadowPool',
             note='enlarged pool (shadow mode)')
    pool = [(CX + (760 + 40 * math.sin(7 * a)) * math.cos(a), 4330 + (120 + 14 * math.sin(5 * a)) * math.sin(a))
            for a in (2 * math.pi * i / 120 for i in range(120))]
    p.fill(pool, ('r', hexc('0c0a10', 245), hexc('2a1a38', 200), CX, 4330, 760))
    p.stroke(pool, G, 6, closed=True)
    add(p)
    for side, f, s in SIDES:
        tend = f([(1150, 4330), (1060, 4130), (1100, 3960), (1020, 3800)])
        p = Part(f'Shadow{"Left" if side == "L" else "Right"}', '02_SHADOW_POOL', visible=False, toggle='mode:shadow',
                 physics='tendril wave', param=f'Param_ShadowTendril{side}')
        p.fill(band(tend, 110, 10), ('v', PURP, hexc('0c0a10'), 3800, 4330), outline=G, ow=5)
        add(p)

    # 03 back hair -------------------------------------------------------------------------
    back = [(1536, 360), (1722, 392), (1842, 500), (1884, 660), (1876, 860), (1846, 1040)] + \
        [(1800, 1130), (1740, 1080), (1680, 1150), (1610, 1090), (1536, 1140), (1462, 1090), (1392, 1150), (1332, 1080), (1272, 1130)] + \
        [(1226, 1040), (1196, 860), (1188, 660), (1230, 500), (1350, 392)]
    p = Part('Hair_BackMain', '03_BACK_HAIR', physics='back hair sway', param='Param_HairBack',
             restore='full back-of-head mass behind face / hood')
    p.fill(back, ('v', HAIR_T, HAIR_B, 360, 1150), outline=HAIR_LN, ow=9)
    p.shade(shift(back, 0, 140), hexc('0a0a0d', 110), blur=16)
    add(p)
    for side, f, s in SIDES:
        path = f([(1250, 900), (1230, 1060), (1250, 1200), (1215, 1290)])
        p = Part(f'Hair_Back{side}', '03_BACK_HAIR', physics='hair tip swing', param=f'Param_HairBack{side}',
                 restore='root under back main')
        p.fill(band(path, 130, 12 + (6 if side == 'R' else 0)), ('v', HAIR_T, HAIR_B, 900, 1290), outline=HAIR_LN, ow=8)
        add(p)

    # 04 hood back -------------------------------------------------------------------------
    hood_down = [(1270, 1130), (1330, 1045), (1440, 1010), (1536, 1030), (1632, 1010), (1742, 1045), (1802, 1130),
                 (1780, 1230), (1680, 1260), (1536, 1250), (1392, 1260), (1292, 1230)]
    p = Part('HoodDown', '04_HOOD_BACK', toggle='hood:down', physics='hood bounce', param='Param_Hood',
             restore='full fold behind neck/hair', note='hood resting on shoulders')
    p.fill(hood_down, ('v', JK_T, JK_B, 1010, 1260), outline=JK_LN, ow=9)
    p.shade(shift(hood_down, 0, 50), SHADE, blur=10)
    p.stroke([(1330, 1110), (1440, 1070), (1536, 1085), (1632, 1070), (1742, 1110)], hexc('2fd592', 200), 5)
    add(p)
    hood_up = [(1536, 250), (1760, 290), (1920, 420), (1990, 640), (1985, 900), (1930, 1120), (1850, 1250),
               (1536, 1280), (1222, 1250), (1142, 1120), (1087, 900), (1082, 640), (1152, 420), (1312, 290)]
    p = Part('HoodUp_Back', '04_HOOD_BACK', visible=False, toggle='hood:up', param='Param_Hood',
             note='inside of raised hood (behind head)')
    p.fill(hood_up, ('v', hexc('17181c'), hexc('0d0d10'), 250, 1280), outline=JK_LN, ow=9)
    add(p)

    # 05 body ---------------------------------------------------------------------------------
    neck = [(1478, 900), (1594, 900), (1604, 1150), (1468, 1150)]
    p = Part('Neck', '05_BODY', param='Param_AngleX/Y (neck deform)', restore='neck under hair, jaw and collar')
    p.fill(neck, SKIN, smooth=False, outline=SKIN_L, ow=5)
    add(p)
    p = Part('NeckShadow', '05_BODY', blend='multiply', param='Param_AngleY', note='jaw cast shadow')
    p.fill([(1470, 940), (1602, 940), (1602, 1040), (1536, 1070), (1470, 1040)], hexc('d0a5a0'))
    p.clip(neck, smooth=False)
    add(p)
    torso = [(1352, 1110), (1720, 1110), (1756, 1300), (1742, 1900), (1330, 1900), (1316, 1300)]
    p = Part('Torso', '05_BODY', param='Param_BodyAngleX/Y, Param_Breath', restore='whole torso under jacket + arms')
    p.fill(torso, ('v', INNER, hexc('202228'), 1110, 1900), outline=JK_LN, ow=7)
    p.shade([(1600, 1110), (1760, 1110), (1760, 1900), (1640, 1900)], SHADE, blur=20)
    add(p)
    for side, f, s in SIDES:
        p = Part(f'Shoulder_{side}', '05_BODY', param=f'Param_Shoulder{side}', restore='shoulder joint under sleeve cap')
        p.fill(f(ellipse_pts(1300, 1250, 95, 90)), INNER, outline=JK_LN, ow=6)
        add(p)
        p = Part(f'UpperArm_{side}', '05_BODY', param=f'Param_Arm{side}A', restore='upper arm inside sleeve')
        p.fill(band(f([(1265, 1230), (1205, 1450), (1165, 1670)]), 120, 100), SKIN, outline=SKIN_L, ow=5)
        add(p)
        p = Part(f'Forearm_{side}', '05_BODY', param=f'Param_Arm{side}B', restore='forearm inside sleeve + wrist under cuff')
        fa = f([(1150, 1700), (1110, 1900), (1080, 2080), (1070, 2170)])
        p.fill(band(fa, 96, 72), SKIN, outline=SKIN_L, ow=5)
        p.shade(band(shift(fa, 22 * s, 0), 50, 30), SKIN_S, blur=6)
        add(p)

    # 06 clothes ------------------------------------------------------------------------------
    jb = [(1236, 1170), (1836, 1170), (1886, 1500), (1900, 1975), (1172, 1975), (1186, 1500)]
    p = Part('JacketBack', '06_CLOTHES', param='Param_BodyAngleX', restore='inside/back of jacket behind torso',
             note='jacket lining + back panel')
    p.fill(jb, ('v', hexc('1b1c21'), hexc('131317'), 1170, 1975), outline=JK_LN, ow=8)
    add(p)
    for side, f, s in SIDES:
        shoe = f([(1378, 3920), (1504, 3920), (1520, 4090), (1532, 4240), (1528, 4330), (1336, 4340), (1320, 4280),
                  (1342, 4150), (1368, 4020)])
        p = Part(f'Shoe{side}', '06_CLOTHES', param=f'Param_Leg{side}', restore='ankle under pants hem')
        p.fill(shoe, ('v', hexc('26272d'), hexc('17171b'), 3920, 4340), outline=JK_LN, ow=8)
        p.fill(f([(1318, 4270), (1532, 4262), (1530, 4336), (1334, 4344)]), hexc('c9ccd4'), outline=JK_LN, ow=6)
        p.stroke(f([(1350, 4200), (1430, 4140), (1515, 4190)]), G, 6, clip=True)
        for k in range(3):
            p.stroke(f([(1400, 4000 + k * 45), (1480, 4000 + k * 45)]), hexc('5c5f69'), 6, smooth=False, clip=True)
        add(p)
    for side, f, s in SIDES:
        leg = f([(1372, 1880), (1540, 1880), (1548, 2150), (1526, 2600), (1508, 3100), (1498, 3500), (1494, 3960),
                 (1388, 3960), (1376, 3500), (1356, 3000), (1340, 2500), (1348, 2150)])
        p = Part(f'Pants{side}', '06_CLOTHES', param=f'Param_Leg{side}', restore='hip overlap + upper leg under jacket/belt')
        p.fill(leg, ('v', PANTS_T, PANTS_B, 1880, 3960), outline=JK_LN, ow=8)
        p.shade(f([(1470, 1880), (1550, 1880), (1530, 3960), (1470, 3960)]), SHADE, blur=14)
        p.stroke(f([(1450, 2500), (1440, 2650), (1440, 2900)]), hexc('1a1b20'), 5, clip=True)  # crease
        p.stroke(f([(1410, 3600), (1440, 3640), (1480, 3600)]), hexc('1a1b20'), 5, clip=True)
        add(p)
        pk = f([(1335, 2380), (1440, 2380), (1445, 2640), (1340, 2640)])
        p = Part(f'PantsPocket{side}', '06_CLOTHES', param=f'Param_Leg{side}', note='cargo pocket')
        p.fill(pk, hexc('2b2d34'), smooth=False, outline=JK_LN, ow=6)
        p.fill(f([(1330, 2370), (1448, 2370), (1448, 2430), (1330, 2430)]), hexc('34363e'), smooth=False, outline=JK_LN, ow=5)
        if side == 'R':
            p.fill(ellipse_pts(1536 + 1536 - 1390, 2400, 12, 12), G)
        add(p)
    inner_pts = [(1356, 1120), (1716, 1120), (1752, 1300), (1742, 1890), (1330, 1890), (1320, 1300)]
    p = Part('Inner', '06_CLOTHES', param='Param_Breath', restore='full shirt behind jacket panels',
             note='very dark gray high-neck inner')
    p.fill(inner_pts, ('v', hexc('2e3037'), hexc('1f2126'), 1120, 1890), outline=JK_LN, ow=7)
    for k in range(4):
        p.stroke([(1400 + k * 80, 1500), (1420 + k * 80, 1800)], hexc('3a3c44'), 5, clip=True)
    add(p)
    p = Part('InnerCollar', '06_CLOTHES', param='Param_AngleX (0.3)', note='high neck', restore='collar back behind neck')
    ic = [(1462, 1030), (1610, 1030), (1622, 1170), (1450, 1170)]
    p.fill(ic, ('v', hexc('33353d'), hexc('24262c'), 1030, 1170), smooth=False, outline=JK_LN, ow=7)
    for k in range(3):
        p.stroke([(1462, 1070 + k * 34), (1610, 1070 + k * 34)], hexc('1c1d22'), 5, smooth=False, clip=True)
    add(p)
    p = Part('Waist', '06_CLOTHES', param='Param_BodyAngleX', note='pants waistband')
    p.fill([(1344, 1850), (1728, 1850), (1732, 1930), (1340, 1930)], hexc('2a2b31'), smooth=False, outline=JK_LN, ow=6)
    add(p)
    p = Part('Belt', '06_CLOTHES', param='Param_BodyAngleX', note='shadow belt with crescent buckle')
    p.fill([(1336, 1872), (1736, 1872), (1740, 1918), (1332, 1918)], hexc('131316'), smooth=False)
    p.fill(ellipse_pts(1536, 1895, 42, 34), hexc('2c2e36'), outline=JK_LN, ow=5)
    cres = arc_pts(1536, 1895, 26, 22, 60, 300, 20) + arc_pts(1546, 1895, 18, 16, 290, 70, 20)
    p.fill(cres, G, smooth=False)
    add(p)
    p = Part('Strap_Thigh', '06_CLOTHES', physics='strap swing', param='Param_Strap1', note='thin thigh strap (L)')
    p.fill(band([(1340, 2200), (1450, 2230), (1540, 2210)], 26, 26), hexc('141417'), outline=JK_LN, ow=4)
    p.fill([(1440, 2210), (1470, 2210), (1470, 2255), (1440, 2255)], hexc('6b6e78'), smooth=False)
    add(p)
    p = Part('Strap_Hanging', '06_CLOTHES', physics='strap pendulum', param='Param_Strap2', note='hanging belt strap (R)')
    p.fill(band([(1690, 1915), (1705, 2080), (1690, 2230)], 30, 26), hexc('141417'), outline=JK_LN, ow=4)
    p.fill([(1675, 2210), (1710, 2210), (1710, 2250), (1675, 2250)], hexc('6b6e78'), smooth=False)
    add(p)
    p = Part('Charm', '06_CLOTHES', physics='charm pendulum', param='Param_Charm', note='spectral crescent charm on belt')
    p.stroke([(1400, 1915), (1398, 1990), (1400, 2040)], hexc('8a8e99'), 5)
    cc = arc_pts(1400, 2090, 48, 48, 40, 320, 24) + arc_pts(1420, 2085, 36, 36, 310, 50, 24)
    p.fill(cc, ('v', hexc('3d2552'), hexc('1a1422'), 2040, 2140), smooth=False, outline=hexc('c9ccd4'), ow=5)
    p.fill(ellipse_pts(1392, 2092, 14, 18), G)
    add(p)
    for side, f, s in SIDES:
        jp = f([(1466, 1150), (1400, 1112), (1300, 1150), (1242, 1210), (1214, 1420), (1206, 1700), (1200, 1975),
                (1486, 1985), (1500, 1650), (1486, 1330)])
        p = Part(f'Jacket{side}', '06_CLOTHES', param='Param_BodyAngleX/Y', restore='panel continues under collar + sleeve',
                 note='oversized short hooded jacket panel')
        p.fill(jp, ('v', JK_T, JK_B, 1110, 1985), outline=JK_LN, ow=9)
        p.shade(f([(1206, 1150), (1300, 1150), (1300, 1985), (1200, 1985)]), SHADE, blur=20)
        p.fill(f([(1200, 1900), (1488, 1908), (1486, 1985), (1200, 1975)]), hexc('1f2025'), outline=JK_LN, ow=6)  # hem rib
        for k in range(1, 6):
            p.stroke(f([(1200 + k * 48, 1910), (1200 + k * 48, 1978)]), hexc('2c2d33'), 4, smooth=False, clip=True)
        if side == 'R':
            p.stroke(f([(1482, 1330), (1496, 1650), (1484, 1905)]), hexc('8a8e99'), 6, clip=True)  # zipper
            p.fill(f([(1474, 1360), (1492, 1360), (1490, 1420), (1476, 1420)]), hexc('b8bcc6'), smooth=False)
        else:
            p.fill([(1250, 1500), (1400, 1500), (1400, 1700), (1250, 1700)], hexc('2b2c33'), smooth=False, outline=JK_LN, ow=5)
        add(p)
        p = Part(f'JacketSeam{side}', '06_CLOTHES', param='Param_Seam (glow in SHADOW)', note='soft spectral-green seam line')
        p.stroke(f([(1478, 1170), (1492, 1330), (1504, 1650), (1490, 1900)]), hexc('34d998'), 6)
        p.stroke(f([(1240, 1230), (1222, 1600), (1214, 1895)]), hexc('34d998', 190), 5)
        add(p)
        cl = f([(1466, 1060), (1412, 1092), (1372, 1160), (1398, 1206), (1466, 1196), (1494, 1120)])
        p = Part(f'Collar{side}', '06_CLOTHES', param='Param_AngleX (0.2)', physics='collar flap')
        p.fill(cl, ('v', hexc('3b3d46'), JK_B, 1040, 1270), outline=JK_LN, ow=8)
        add(p)
    # 07 arms (sleeves / cuffs / hands, above jacket body) -------------------------------------
    for side, f, s in SIDES:
        up = f([(1268, 1200), (1205, 1450), (1160, 1690)])
        p = Part(f'SleeveUpper{side}', '07_ARMS', physics='sleeve swing', param=f'Param_Arm{side}A',
                 restore='cap continues under collar')
        p.fill(band(up, 210, 180), ('v', JK_T, JK_B, 1200, 1690), outline=JK_LN, ow=9)
        p.shade(band(shift(up, -40 * s, 0), 90, 70), SHADE, blur=14)
        p.stroke(f([(1250, 1300), (1230, 1420)]), hexc('1a1b20'), 5, clip=True)
        add(p)
        lo = f([(1162, 1660), (1118, 1880), (1090, 2060)])
        p = Part(f'SleeveLower{side}', '07_ARMS', physics='sleeve swing 2', param=f'Param_Arm{side}B',
                 restore='elbow overlap under upper sleeve')
        p.fill(band(lo, 182, 160), ('v', JK_T, JK_B, 1660, 2060), outline=JK_LN, ow=9)
        p.shade(band(shift(lo, -35 * s, 0), 70, 60), SHADE, blur=12)
        p.stroke(f([(1125, 1760), (1160, 1800), (1135, 1840)]), hexc('1a1b20'), 5, clip=True)
        add(p)
        cf = f([(1094, 2030), (1080, 2110)])
        p = Part(f'Cuff{side}', '07_ARMS', param=f'Param_Arm{side}B', note='rib cuff with green line')
        p.fill(band(cf, 150, 142), hexc('1f2025'), outline=JK_LN, ow=7)
        p.stroke(f([(1020, 2080), (1150, 2090)]), G, 5, clip=True)
        add(p)
        hand = f([(1030, 2120), (1120, 2118), (1142, 2200), (1140, 2300), (1118, 2370), (1088, 2395), (1058, 2385),
                  (1034, 2350), (1020, 2270), (1016, 2190)])
        p = Part(f'Hand{side}', '07_ARMS', param=f'Param_Hand{side}', restore='palm root under cuff')
        p.fill(hand, SKIN, outline=SKIN_L, ow=5)
        for k in range(3):
            p.stroke(f([(1052 + k * 24, 2300), (1056 + k * 24, 2375)]), SKIN_L, 4, clip=True)
        p.shade(shift(hand, 28 * s, 0), SKIN_S, blur=8)
        add(p)
        p = Part(f'Glove{side}', '07_ARMS', param=f'Param_Hand{side}', note='fingerless spectral glove')
        gl = f([(1026, 2120), (1124, 2118), (1144, 2200), (1142, 2290), (1020, 2290), (1014, 2190)])
        p.fill(gl, ('v', hexc('24252b'), hexc('17171b'), 2120, 2290), outline=JK_LN, ow=6)
        p.stroke(f([(1030, 2270), (1135, 2270)]), G, 5, clip=True)
        p.fill(f(ellipse_pts(1080, 2200, 16, 16)), hexc('34d998'))
        add(p)
        fist = f(ellipse_pts(1076, 2230, 78, 92))
        p = Part(f'Fist{side}', '07_ARMS', visible=False, toggle='mode:combat|pose:fist', param=f'Param_Hand{side}Fist',
                 note='clenched gloved fist swap (combat)')
        p.fill(fist, SKIN, outline=SKIN_L, ow=6)
        p.fill(f([(1000, 2140), (1152, 2140), (1156, 2270), (996, 2270)]), hexc('1c1d22'), outline=JK_LN, ow=6)
        for k in range(4):
            p.stroke(f(arc_pts(1022 + k * 36, 2290, 18, 16, 0, 180, 10)), SKIN_L, 5)
        p.stroke(f([(1004, 2250), (1150, 2250)]), G, 6, clip=True)
        add(p)

    # 08 face ------------------------------------------------------------------------------------
    for side, f, s in SIDES:
        ear = f([(1308, 742), (1276, 752), (1262, 800), (1272, 858), (1300, 880), (1318, 870)])
        p = Part(f'Ear_{side}', '08_FACE', param='Param_AngleX', restore='ear root under side hair')
        p.fill(ear, SKIN, outline=SKIN_L, ow=5)
        p.stroke(f([(1296, 772), (1282, 805), (1292, 845)]), SKIN_L, 4)
        if side == 'L':
            p.fill(ellipse_pts(1282, 860, 8, 8), hexc('2fd592'))  # single ear stud (asym)
        add(p)
    p = Part('Face_Base', '08_FACE', param='Param_AngleX/Y/Z', restore='forehead + temples under bangs')
    p.fill(FACE, SKIN, outline=SKIN_L, ow=6)
    p.shade([(1700, 700), (1780, 700), (1780, 1020), (1640, 1020)], hexc('e3bba9', 120), blur=30)
    add(p)
    p = Part('Face_Shadow', '08_FACE', blend='multiply', param='Param_AngleY', note='hair cast shadow on forehead/cheeks')
    p.fill([(1300, 560), (1772, 560), (1772, 700), (1700, 680), (1600, 740), (1536, 700), (1460, 740), (1360, 690), (1300, 720)],
           hexc('dcb0a8'), blur=8)
    p.clip(FACE)
    add(p)
    p = Part('Nose', '08_FACE', param='Param_AngleX')
    p.stroke([(1548, 880), (1554, 898), (1544, 904)], hexc('c48e82'), 5)
    add(p)
    for side, f, s in SIDES:
        p = Part(f'Blush_{side}', '08_FACE', visible=False, toggle='fx:blush', param='Param_Cheek')
        p.glow(f(ellipse_pts(1415, 895, 58, 26)), hexc('ff8fa6', 150), 10)
        for k in range(3):
            p.stroke(f([(1385 + k * 26, 910), (1400 + k * 26, 880)]), hexc('f0708c', 200), 4, smooth=False)
        add(p)

    # 09 eyes ----------------------------------------------------------------------------------
    for side, f, s in SIDES:
        scl = f(SCL_L)
        ix = EYE_L[0] if side == 'L' else 2 * CX - EYE_L[0]
        iy = EYE_L[1]
        p = Part(f'Eye{side}_Sclera', '09_EYES', param=f'Param_EyeOpen{side}', restore='full sclera under lids/lashes')
        p.fill(scl, WHITE)
        p.shade(shift(scl, 0, -34), hexc('c9cdd9', 200), blur=4)
        add(p)
        p = Part(f'Eye{side}_Sclera_Dark', '09_EYES', visible=False, toggle='mode:od', param='Param_Overdrive',
                 note='subtle black-sclera treatment (overdrive)')
        p.fill(scl, ('v', hexc('24222b'), hexc('0e0d12'), 750, 850))
        add(p)
        p = Part(f'Eye{side}_Iris', '09_EYES', param='Param_EyeBallX/Y', restore='full iris circle under lids')
        p.fill(ellipse_pts(ix, iy, 44, 54), ('r', IRIS_C, IRIS_E, ix - 6, iy + 10, 60), outline=hexc('14191c'), ow=4)
        p.shade(shift(scl, 0, -40), hexc('0e1417', 130), blur=4)
        p.clip(scl)
        add(p)
        p = Part(f'Eye{side}_Iris_Spectral', '09_EYES', visible=False, toggle='mode:shadow', param='Param_ShadowEyes',
                 note='iris shifts to spectral teal-green')
        p.fill(ellipse_pts(ix, iy, 44, 54), ('r', hexc('7df2c8'), hexc('0b5a47'), ix - 6, iy + 12, 60), outline=hexc('06231c'), ow=4)
        p.shade(shift(scl, 0, -42), hexc('03120d', 120), blur=4)
        p.clip(scl)
        add(p)
        p = Part(f'Eye{side}_Pupil', '09_EYES', param='Param_EyeBallX/Y')
        p.fill(ellipse_pts(ix, iy + 4, 16, 24), ('r', hexc('26343a'), hexc('07090b'), ix - 8, iy - 6, 26))
        p.shade(shift(scl, 0, -44), hexc('000000', 120), blur=3)
        p.clip(scl)
        add(p)
        p = Part(f'Eye{side}_ShadowRing', '09_EYES', visible=False, toggle='mode:shadow', param='Param_ShadowEyes',
                 note='spectral green inner ring')
        p.stroke(ellipse_pts(ix, iy, 30, 38), ('r', G2, GD, ix - 20, iy - 26, 80), 6, closed=True)
        p.shade(shift(scl, 0, -44), hexc('03120d', 110), blur=3)
        p.clip(scl)
        add(p)
        p = Part(f'Eye{side}_OverdriveRing', '09_EYES', visible=False, toggle='mode:od', param='Param_Overdrive',
                 note='second (outer) spectral ring')
        p.stroke(ellipse_pts(ix, iy, 42, 51), G2, 5, closed=True)
        p.clip(scl)
        add(p)
        p = Part(f'Eye{side}_Highlight01', '09_EYES', param='Param_EyeBallX/Y (0.4)')
        p.fill(ellipse_pts(ix - 14, iy - 22, 12 + (1 if side == 'R' else 0), 10), WHITE)
        add(p)
        p = Part(f'Eye{side}_Highlight02', '09_EYES', param='Param_EyeBallX/Y (0.4)')
        p.fill(ellipse_pts(ix + 16, iy + 24, 6, 5 + (1 if side == 'L' else 0)), hexc('ffffff', 220))
        add(p)
        p = Part(f'Eye{side}_UpperLash', '09_EYES', param=f'Param_EyeOpen{side}')
        p.fill(band(f([(1364, 810), (1384, 766), (1440, 744), (1496, 754), (1518, 790)]), 12, 16), LASH)
        p.fill(f([(1368, 800), (1340, 790), (1376, 776)]), LASH, smooth=False)
        add(p)
        p = Part(f'Eye{side}_LowerLash', '09_EYES', param=f'Param_EyeOpen{side}')
        p.stroke(f([(1402, 840), (1440, 850), (1482, 838)]), hexc('4a3a40'), 4)
        add(p)
        p = Part(f'Eye{side}_UpperLid', '09_EYES', param=f'Param_EyeOpen{side}', note='lid crease (deform for blink)')
        p.stroke(f([(1392, 742), (1440, 728), (1494, 738)]), hexc('c08b80'), 4)
        add(p)
        p = Part(f'Eye{side}_LowerLid', '09_EYES', param=f'Param_EyeSmile{side}', note='lower lid skin (smile squint)')
        p.fill(f([(1392, 846), (1440, 858), (1488, 842), (1492, 860), (1440, 876), (1390, 864)]), hexc('ecc6b6'))
        add(p)
        p = Part(f'Eye{side}_Close', '09_EYES', visible=False, toggle='eye:closed', param=f'Param_EyeOpen{side}=0')
        p.stroke(f([(1366, 812), (1400, 826), (1440, 832), (1482, 826), (1514, 808)]), LASH, 9)
        p.stroke(f([(1370, 812), (1352, 822)]), LASH, 6)
        add(p)
        p = Part(f'Eye{side}_Smile', '09_EYES', visible=False, toggle='eye:smile', param=f'Param_EyeSmile{side}')
        p.stroke(f([(1372, 830), (1406, 800), (1440, 790), (1476, 800), (1510, 828)]), LASH, 9)
        add(p)
        p = Part(f'Eye{side}_HalfLid', '09_EYES', visible=False, toggle='eye:half', param=f'Param_EyeOpen{side}=0.5',
                 note='skin lid covering top half (deadpan/sleepy/annoyed)')
        p.fill(f([(1360, 700), (1520, 700), (1520, 790), (1440, 796), (1360, 800)]), SKIN)
        p.clip(scale(scl, 1.25, 1.6, ix, iy + 10))
        p.stroke(f([(1370, 800), (1440, 794), (1512, 788)]), LASH, 9)
        add(p)
        p = Part(f'Eye{side}_Tear', '09_EYES', visible=False, toggle='fx:tear', physics='tear drip', param='Param_Tear')
        p.fill(f([(1400, 846), (1480, 846), (1470, 870), (1440, 876), (1408, 868)]), hexc('bfe8ff', 220))
        p.fill(band(f([(1400, 860), (1394, 940), (1400, 1000)]), 14, 22), hexc('9ed8ff', 220))
        add(p)

    # 10 brows ---------------------------------------------------------------------------------
    brows = {
        'Brow': ([(1374, 706), (1430, 690), (1494, 700)], None, ''),
        'Brow_Angry': ([(1380, 684), (1440, 700), (1500, 726)], 'brow:angry', 'Param_BrowForm=-1'),
        'Brow_Sad': ([(1378, 722), (1436, 704), (1494, 682)], 'brow:sad', 'Param_BrowForm=+1'),
        'Brow_Up': ([(1374, 672), (1432, 652), (1494, 664)], 'brow:up', 'Param_BrowY=+1'),
    }
    for nm, (pts, tg, prm) in brows.items():
        for side, f, s in SIDES:
            p = Part(f'{nm}_{side}', '10_BROWS', visible=tg is None, toggle=tg or 'brow:neutral',
                     param=prm or f'Param_Brow{side}Y/Angle')
            p.fill(band(f(pts), 16, 8), hexc('2b2c33'))
            add(p)

    # 11 mouth ---------------------------------------------------------------------------------
    MY = 950
    p = Part('Mouth_Line', '11_MOUTH', toggle='mouth:neutral', param='Param_MouthForm / MouthOpenY=0')
    p.stroke([(1512, MY), (1536, MY + 4), (1562, MY - 1)], hexc('8a4a50'), 5)
    add(p)
    mo = [(1500, MY - 8), (1536, MY - 4), (1572, MY - 8), (1562, MY + 22), (1536, MY + 34), (1510, MY + 22)]
    p = Part('Mouth_Inner', '11_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthOpenY')
    p.fill(mo, hexc('5a1f2a'))
    add(p)
    p = Part('Mouth_Teeth', '11_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthOpenY')
    p.fill([(1500, MY - 10), (1572, MY - 10), (1566, MY + 2), (1506, MY + 2)], WHITE)
    p.clip(mo)
    add(p)
    p = Part('Mouth_Tongue', '11_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthOpenY/Form')
    p.fill(ellipse_pts(1536, MY + 30, 26, 14), hexc('e27b86'))
    p.clip(mo)
    add(p)
    p = Part('Mouth_UpperLip', '11_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthForm')
    p.stroke(mo[:3], hexc('7a3e44'), 5)
    add(p)
    p = Part('Mouth_LowerLip', '11_MOUTH', visible=False, toggle='mouth:open', param='Param_MouthOpenY')
    p.stroke([mo[2], mo[3], mo[4], mo[5], mo[0]], hexc('b0707a'), 4)
    add(p)
    p = Part('Mouth_Shadow', '11_MOUTH', blend='multiply', visible=False, toggle='mouth:open', param='Param_MouthOpenY')
    p.glow(ellipse_pts(1536, MY + 50, 34, 8), hexc('e0b0a4'), 3)
    add(p)
    mouths = {
        'Mouth_Smile': ('mouth:smile', [(1506, MY - 8), (1536, MY + 8), (1566, MY - 8)]),
        'Mouth_Frown': ('mouth:frown', [(1510, MY + 8), (1536, MY - 4), (1562, MY + 8)]),
        'Mouth_Smirk': ('mouth:smirk', [(1508, MY + 2), (1540, MY + 4), (1570, MY - 12)]),
        'Mouth_Wavy': ('mouth:wavy', [(1500 + 12 * k, MY + (5 if k % 2 else -4)) for k in range(7)]),
        'Mouth_Flat': ('mouth:flat', [(1508, MY + 2), (1564, MY + 2)]),
    }
    for nm, (tg, pts) in mouths.items():
        p = Part(nm, '11_MOUTH', visible=False, toggle=tg, param='Param_MouthForm')
        p.stroke(pts, hexc('7a3e44'), 5, smooth=nm != 'Mouth_Flat')
        add(p)
    p = Part('Mouth_O', '11_MOUTH', visible=False, toggle='mouth:o', param='Param_MouthOpenY')
    p.fill(ellipse_pts(1536, MY + 8, 16, 20), hexc('5a1f2a'), outline=hexc('7a3e44'), ow=4)
    add(p)
    p = Part('Mouth_Fang', '11_MOUTH', visible=False, toggle='mouth:fang', param='Param_MouthForm')
    p.fill([(1550, MY - 2), (1562, MY - 2), (1556, MY + 12)], WHITE, smooth=False)
    add(p)

    # 12 front hair ---------------------------------------------------------------------------
    for side, f, s in SIDES:
        path = f([(1336, 540), (1300, 700), (1286, 880), (1296, 1040), (1276, 1110)])
        p = Part(f'Hair_Side{side}', '12_FRONT_HAIR', physics='side lock sway', param=f'Param_HairSide{side}',
                 restore='root under front cap')
        p.fill(band(path, 124, 10 + (8 if side == 'R' else 0)), ('v', HAIR_T, HAIR_B, 540, 1110), outline=HAIR_LN, ow=8)
        p.shade(band(shift(path, 22 * s, 0), 50, 6), hexc('0a0a0d', 100), blur=6)
        add(p)
    locks = {
        'Hair_FrontL1': [(1392, 560), (1478, 560), (1466, 680), (1428, 796), (1402, 740), (1384, 640)],
        'Hair_FrontL2': [(1306, 560), (1386, 560), (1374, 700), (1334, 850), (1310, 730)],
        'Hair_FrontR1': [(1594, 560), (1686, 560), (1676, 660), (1650, 770), (1628, 720), (1606, 640)],
        'Hair_FrontR2': [(1690, 560), (1768, 560), (1766, 720), (1742, 880), (1716, 760)],
    }
    for nm, pts in locks.items():
        p = Part(nm, '12_FRONT_HAIR', physics='bang strand sway', param=f'Param_{nm}', restore='root under cap')
        p.fill(pts, ('v', HAIR_T, HAIR_B, 560, 880), outline=HAIR_LN, ow=7)
        add(p)
    cap = [(1290, 700), (1296, 540), (1380, 440), (1536, 398), (1692, 440), (1776, 540), (1782, 700), (1716, 620),
           (1650, 650), (1590, 720), (1548, 820), (1508, 712), (1450, 648), (1380, 624)]
    p = Part('Hair_FrontCenter', '12_FRONT_HAIR', physics='bangs sway (center)', param='Param_HairFront',
             note='bang cap + center lock')
    p.fill(cap, ('v', HAIR_T, HAIR_B, 398, 820), outline=HAIR_LN, ow=8)
    p.shade(shift(cap, 0, 70), hexc('0a0a0d', 90), blur=10)
    add(p)
    p = Part('Hair_Accent_Smoke', '12_FRONT_HAIR', physics='smoke strand (loose)', param='Param_HairAccent',
             note='crown strand with smoke-curl tip (original, not the Pokémon crest)')
    p.fill(band([(1560, 430), (1590, 340), (1660, 300), (1720, 320), (1710, 370), (1672, 360)], 56, 8),
           ('v', HAIR_T, HAIR_B, 300, 430), outline=HAIR_LN, ow=6)
    add(p)
    p = Part('Hair_Strand_Physics', '12_FRONT_HAIR', physics='long physics strand', param='Param_HairStrand',
             note='loose strand across R cheek with smoky tip')
    p.fill(band([(1740, 620), (1770, 780), (1760, 920), (1790, 1030), (1760, 1080)], 40, 6), ('v', HAIR_T, HAIR_B, 620, 1080),
           outline=HAIR_LN, ow=5)
    add(p)
    p = Part('Hair_Highlight', '12_FRONT_HAIR', blend='screen', param='Param_AngleX (0.5)', note='angel-ring highlight')
    for a0, a1 in ((200, 235), (245, 290), (300, 335)):
        p.stroke(arc_pts(CX, 640, 230, 150, a0, a1, 14), hexc('4a4f5e'), 14)
    add(p)
    for i, (path) in enumerate([[(1276, 1110), (1296, 1040)], [(1760, 1080), (1790, 1030)], [(1672, 360), (1720, 320)]], 1):
        p = Part(f'HairGlow_Tip0{i}', '12_FRONT_HAIR', blend='add', visible=False, toggle='mode:od', param='Param_Overdrive',
                 note='spectral hair-tip glow (overdrive)')
        x, y = path[0]
        p.glow(ellipse_pts(x, y, 40 + 6 * i, 46), hexc('36e6a0', 220), 14)
        p.glow(ellipse_pts(x, y, 16, 16), G2, 4)
        add(p)

    # 13 hood up ---------------------------------------------------------------------------------
    rim = [(1536, 250), (1760, 290), (1920, 420), (1990, 640), (1985, 900), (1930, 1120), (1850, 1250), (1760, 1180),
           (1830, 1000), (1848, 760), (1810, 540), (1700, 420), (1536, 390), (1372, 420), (1262, 540), (1224, 760),
           (1242, 1000), (1312, 1180), (1222, 1250), (1142, 1120), (1087, 900), (1082, 640), (1152, 420), (1312, 290)]
    p = Part('HoodUp_Front', '13_HOOD_UP', visible=False, toggle='hood:up', physics='hood bounce', param='Param_Hood',
             note='raised hood rim framing face (face/eyes/bangs stay visible)')
    p.fill(rim, ('v', JK_T, JK_B, 250, 1250), outline=JK_LN, ow=9)
    p.shade(shift(rim, 60, 0), SHADE, blur=16)
    p.stroke([(1262, 540), (1372, 420), (1536, 390), (1700, 420), (1810, 540)], hexc('34d998'), 6)
    add(p)
    for side, f, s in SIDES:
        p = Part(f'HoodUp_Peak_{side}', '13_HOOD_UP', visible=False, toggle='hood:up', physics='peak flop',
                 param=f'Param_HoodPeak{side}', note='soft swirl-stitched hood peak')
        pk = f([(1150, 440), (1100, 330), (1130, 220), (1210, 190), (1250, 250), (1230, 320), (1290, 330)])
        p.fill(pk, ('v', JK_T, JK_B, 190, 440), outline=JK_LN, ow=8)
        sp = [(1190 + (7 * t) * math.cos(t * 0.7) * s, 290 + (7 * t) * math.sin(t * 0.7)) for t in range(2, 9)]
        p.stroke(sp, hexc('34d998'), 5)
        add(p)

    # 14 shadow ------------------------------------------------------------------------------------
    for side, f, s in SIDES:
        hx, hy = (720 if side == 'L' else 2352), 2300
        hand = [(hx - 200, hy + 80), (hx - 190, hy - 100), (hx - 130, hy - 150), (hx - 90, hy - 60), (hx - 70, hy - 300),
                (hx - 10, hy - 320), (hx + 20, hy - 110), (hx + 70, hy - 330), (hx + 135, hy - 300), (hx + 120, hy - 100),
                (hx + 190, hy - 240), (hx + 245, hy - 205), (hx + 200, hy + 40), (hx + 110, hy + 220), (hx - 80, hy + 240)]
        if side == 'R':
            hand = mirror(hand, hx)
        p = Part(f'ShadowHand{side}', '14_SHADOW', visible=False, toggle='mode:combat|fx:shadowhands', physics='hover + follow',
                 param=f'Param_ShadowHand{side}', note='living-shadow hand (combat)')
        p.fill(hand, ('v', hexc('120f18', 240), hexc('2e1d3e', 230), hy - 330, hy + 240), outline=G, ow=8)
        p.shade(shift(hand, 0, 90), hexc('000000', 90), blur=14)
        add(p)
        p = Part(f'ShadowFinger{side}', '14_SHADOW', visible=False, toggle='mode:combat|fx:shadowhands', physics='claw flex',
                 param=f'Param_ShadowFinger{side}', note='glowing claw tips')
        for (x, y) in [(hand[4]), (hand[7]), (hand[10]), (hand[1])]:
            p.fill([(x - 18, y + 30), (x, y - 40), (x + 18, y + 30)], G2, smooth=False, outline=GD, ow=4)
        add(p)
    p = Part('Fragments01', '14_SHADOW', visible=False, toggle='mode:od', physics='orbit', param='Param_Fragments')
    rng = np.random.default_rng(11)
    for _ in range(12):
        x, y = rng.uniform(850, 2220), rng.uniform(1300, 2700)
        if abs(x - CX) < 460:
            continue
        r, a = rng.uniform(22, 50), rng.uniform(0, 360)
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        p.fill([(x + r * c, y + r * s_), (x - r * .35 * s_, y + r * .35 * c), (x - r * c, y - r * s_), (x + r * .45 * s_, y - r * .45 * c)],
               ('v', PURP2, hexc('0e0c13'), y - r, y + r), smooth=False, outline=G, ow=4)
    add(p)
    p = Part('Fragments02', '14_SHADOW', visible=False, toggle='mode:od', physics='orbit (counter)', param='Param_Fragments')
    for _ in range(12):
        x, y = rng.uniform(900, 2170), rng.uniform(2700, 4000)
        if abs(x - CX) < 250:
            continue
        r = rng.uniform(16, 36)
        p.fill([(x, y - r), (x + r * .6, y), (x, y + r * 1.3), (x - r * .6, y)], hexc('130f19', 235), smooth=False, outline=G, ow=4)
    add(p)
    p = Part('CombatAuraLocal', '14_SHADOW', blend='add', visible=False, toggle='mode:combat', param='Param_Combat',
             note='local aura around hands/forearms only (no full-body white aura)')
    for x in (1080, 1992):
        p.glow(ellipse_pts(x, 2180, 170, 260), hexc('1a9a6c', 170), 45)
    add(p)
    p = Part('Mist_Front', '14_SHADOW', visible=False, toggle='mode:od|fx:mist', physics='mist drift', param='Param_Mist')
    for _ in range(7):
        x, y = rng.uniform(1000, 2070), rng.uniform(3950, 4380)
        p.glow(ellipse_pts(x, y, rng.uniform(150, 260), rng.uniform(40, 70)), hexc('241a2e', 150), 30)
    add(p)

    # 15 front fx -------------------------------------------------------------------------------------
    for side, f, s in SIDES:
        ix = EYE_L[0] if side == 'L' else 2 * CX - EYE_L[0]
        p = Part(f'CombatEyeGlow{side}', '15_FRONT_FX', blend='add', visible=False, toggle='mode:combat|fx:eyeglow',
                 param='Param_EyeGlow')
        p.glow(f(scale(SCL_L, 1.3, 1.6, 1440, 800)), hexc('1fbf85', 170), 18)
        p.glow(ellipse_pts(ix, 800, 26, 32), G2, 6)
        add(p)
    p = Part('Particles01', '15_FRONT_FX', blend='add', visible=False, toggle='mode:combat', physics='float up', param='Param_Particles')
    for _ in range(30):
        x, y = rng.uniform(800, 2270), rng.uniform(900, 3600)
        if abs(x - CX) < 420:
            continue
        r = rng.uniform(6, 16)
        p.glow(ellipse_pts(x, y, r, r), G2, 3)
    add(p)
    p = Part('Particles02', '15_FRONT_FX', blend='add', visible=False, toggle='mode:od', physics='float up (fast)', param='Param_Particles')
    for _ in range(26):
        x, y = rng.uniform(850, 2220), rng.uniform(300, 4200)
        if abs(x - CX) < 350:
            continue
        s_ = rng.uniform(12, 28)
        p.glow([(x, y - s_), (x + s_ * .35, y), (x, y + s_), (x - s_ * .35, y)], TQ, 2, smooth=False)
    add(p)
    p = Part('CharmCore_Glow', '15_FRONT_FX', blend='add', visible=False, toggle='mode:combat', param='Param_Combat',
             note='charm/core activation')
    p.glow(ellipse_pts(1395, 2090, 70, 70), hexc('36e6a0', 220), 18)
    add(p)
    p = Part('SeamGlow', '15_FRONT_FX', blend='add', visible=False, toggle='mode:shadow', param='Param_Seam',
             note='jacket seam lines light up')
    for f in (ID, M):
        p.glow(band(f([(1478, 1170), (1492, 1330), (1504, 1650), (1490, 1900)]), 22, 22), hexc('2fe0a0', 170), 8)
        p.glow(band(f([(1240, 1230), (1222, 1600), (1214, 1895)]), 20, 20), hexc('2fe0a0', 150), 8)
    add(p)
    for i, ys in enumerate([(700, 1000, 1500, 2600), (1200, 1900, 2300, 3300)], 1):
        p = Part(f'Glitch0{i}', '15_FRONT_FX', blend='screen', visible=False, toggle='mode:od|fx:glitch',
                 param='Param_Glitch', note='subtle scan-slice glitch')
        for y in ys:
            x0 = rng.uniform(1100, 1500)
            p.fill([(x0, y), (x0 + rng.uniform(250, 600), y), (x0 + rng.uniform(250, 600), y + 14), (x0, y + 14)],
                   hexc('39f0b0', 150) if i == 1 else hexc('9a5cff', 140), smooth=False)
        add(p)

    # 16 expression marks -------------------------------------------------------------------------------
    p = Part('Mark_Embarrass', '16_EXPRESSIONS', visible=False, toggle='fx:embarrass', param='Param_Embarrass')
    for k in range(4):
        p.stroke([(1360 + k * 30, 600 + k * 2), (1372 + k * 30, 660)], hexc('7a88ff', 170), 5, smooth=False)
    add(p)
    p = Part('Mark_Sweat', '16_EXPRESSIONS', visible=False, toggle='fx:sweat', param='Param_Sweat')
    p.fill([(1810, 600), (1836, 670), (1830, 706), (1810, 718), (1790, 706), (1784, 670)], hexc('a5dcff', 235),
           outline=hexc('2a6fb0'), ow=4)
    add(p)
    p = Part('Mark_Anger', '16_EXPRESSIONS', visible=False, toggle='fx:anger', param='Param_Anger')
    for a in (0, 90, 180, 270):
        c, s_ = math.cos(math.radians(a + 45)), math.sin(math.radians(a + 45))
        p.stroke([(1780 + 18 * c, 520 + 18 * s_), (1780 + 42 * c + 14 * s_, 520 + 42 * s_ - 14 * c), (1780 + 46 * c, 520 + 46 * s_)],
                 hexc('ff5a4e'), 10)
    add(p)
    p = Part('Mark_Zzz', '16_EXPRESSIONS', visible=False, toggle='fx:sleep', param='Param_Sleep')
    for i, (x, y, s_) in enumerate([(1820, 560, 34), (1880, 480, 46), (1950, 380, 58)]):
        p.stroke([(x, y), (x + s_, y), (x, y + s_), (x + s_, y + s_)], hexc('b8ecff'), 8 + i, smooth=False)
    add(p)
    p = Part('Mark_Confused', '16_EXPRESSIONS', visible=False, toggle='fx:confused', param='Param_Confused')
    p.stroke([(1830, 470), (1840, 420), (1880, 400), (1915, 425), (1900, 470), (1872, 495), (1872, 530)], hexc('d0d4ff'), 10)
    p.fill(ellipse_pts(1872, 565, 9, 9), hexc('d0d4ff'))
    sp = [(1250 + (5 * t) * math.cos(t * 0.6), 540 + (5 * t) * math.sin(t * 0.6)) for t in range(3, 14)]
    p.stroke(sp, hexc('d0d4ff'), 8)
    add(p)
    p = Part('Mark_Shock', '16_EXPRESSIONS', visible=False, toggle='fx:shock', param='Param_Surprise')
    for a in (-70, -45, -20):
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        for sg in (1, -1):
            p.stroke([(CX + sg * 380 * c, 720 + 380 * s_), (CX + sg * 450 * c, 720 + 450 * s_)], hexc('f2f2f2'), 9, smooth=False)
    add(p)
    p = Part('Mark_Gloom', '16_EXPRESSIONS', blend='multiply', visible=False, toggle='fx:gloom', param='Param_Gloom',
             note='gloom lines on forehead')
    for k in range(6):
        p.stroke([(1400 + k * 52, 540), (1400 + k * 52, 640)], hexc('9a8fb0'), 7, smooth=False)
    p.clip(FACE)
    add(p)
    p = Part('Mark_Sparkle', '16_EXPRESSIONS', visible=False, toggle='fx:sparkle', param='Param_Happy')
    for (x, y, r) in [(1860, 560, 36), (1220, 700, 26), (1830, 900, 20)]:
        p.fill([(x, y - r), (x + r * .25, y - r * .25), (x + r, y), (x + r * .25, y + r * .25), (x, y + r), (x - r * .25, y + r * .25),
                (x - r, y), (x - r * .25, y - r * .25)], hexc('fff7c2'), smooth=False)
    add(p)

    # 17 overdrive --------------------------------------------------------------------------------------
    p = Part('OverdriveLocalGlow', '17_OVERDRIVE', blend='add', visible=False, toggle='mode:od', param='Param_Overdrive',
             note='local eye/halo glow band (not full body)')
    p.glow(ellipse_pts(CX, 800, 330, 70), hexc('0f7a57', 150), 40)
    add(p)
    p = Part('Overdrive_Flame_Front', '17_OVERDRIVE', blend='add', visible=False, toggle='mode:od', physics='flame flicker',
             param='Param_Overdrive', note='green shadow flame licking up from the hands')
    for f in (ID, M):
        p.glow(f([(1020, 2380), (980, 2200), (1010, 2050), (990, 1900), (1060, 1990), (1090, 1850), (1130, 2000),
                  (1160, 2120), (1150, 2380)]), ('v', hexc('b8ffe2', 200), hexc('0e8a60', 60), 1850, 2380), 14)
    add(p)
    return [remap(p) for p in P]


def derived(recs, W, H):
    """ShadowRear: the character's own silhouette as a living shadow (mimicry), offset & tinted."""
    body_groups = {'03_BACK_HAIR', '04_HOOD_BACK', '05_BODY', '06_CLOTHES', '07_ARMS', '08_FACE', '12_FRONT_HAIR'}
    k = 4
    a = np.zeros((H // k, W // k), np.float32)
    for r in recs:
        if r['group'] in body_groups and r['visible'] and r['blend'] == 'normal':
            al = r['img'].getchannel('A').resize((max(1, r['img'].width // k), max(1, r['img'].height // k)), Image.BOX)
            arr = np.asarray(al, np.float32) / 255
            y, x = r['y'] // k, r['x'] // k
            sub = a[y:y + arr.shape[0], x:x + arr.shape[1]]
            sub[:] = np.maximum(sub, arr[:sub.shape[0], :sub.shape[1]])
    sil = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4))
    big = sil.resize((W, H), Image.BILINEAR)
    grad = np.linspace(0.35, 0.9, H)[:, None]
    al = (np.asarray(big, np.float32) * grad).astype(np.uint8)
    img = Image.new('RGBA', (W, H), PURP)
    img.putalpha(Image.fromarray(al))
    img = ImageChops.offset(img, 95, -40)
    bb = img.getchannel('A').point(lambda v: 255 if v > 3 else 0).getbbox()
    p = Part('ShadowRear', '02_SHADOW_POOL', visible=False, toggle='mode:shadow', physics='lag follow (mimicry)',
             param='Param_ShadowRearX/Y', note='living shadow standing behind the body')
    return [(p, img.crop(bb), bb[0], bb[1])]


# ---------------------------------------------------------------------- states
SH = ['mode:shadow']
CB = SH + ['mode:combat', 'pose:fist']
OD = CB + ['mode:od']
HANDS_OFF = ['HandL', 'HandR', 'GloveL', 'GloveR']
EYES_OPEN = [f'Eye{s}_{n}' for s in 'LR' for n in ('Sclera', 'Iris', 'Pupil', 'Highlight01', 'Highlight02', 'UpperLash', 'LowerLash', 'UpperLid')]
EXPR = {
    'Neutral': {},
    'Soft_Smile': {'on': ['mouth:smile', 'eye:none'], 'off': ['mouth:neutral']},
    'Big_Smile': {'on': ['mouth:open', 'fx:blush', 'fx:sparkle'], 'off': ['mouth:neutral']},
    'Laugh': {'on': ['eye:smile', 'mouth:open', 'fx:blush', 'brow:up'], 'off': ['mouth:neutral', 'brow:neutral'] + EYES_OPEN},
    'Mischievous': {'on': ['eye:half', 'mouth:smirk', 'mouth:fang', 'brow:angry'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Surprised': {'on': ['mouth:o', 'brow:up', 'fx:shock'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Embarrassed': {'on': ['mouth:wavy', 'fx:blush', 'fx:embarrass', 'fx:sweat', 'brow:sad'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Annoyed': {'on': ['eye:half', 'mouth:frown', 'brow:angry'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Angry': {'on': ['mouth:open', 'brow:angry', 'fx:anger'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Sad': {'on': ['mouth:frown', 'brow:sad'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Crying': {'on': ['mouth:wavy', 'brow:sad', 'fx:tear'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Sleepy': {'on': ['eye:closed', 'mouth:o', 'fx:sleep'], 'off': ['mouth:neutral'] + EYES_OPEN},
    'Confused': {'on': ['mouth:wavy', 'fx:confused', 'Brow_Up_L', 'Brow_Sad_R'], 'off': ['mouth:neutral', 'brow:neutral']},
    'Deadpan': {'on': ['eye:half', 'mouth:flat', 'fx:gloom'], 'off': ['mouth:neutral']},
    'Shadow': {'on': SH + ['mouth:smirk'], 'off': ['mouth:neutral']},
    'Combat': {'on': CB + ['brow:angry', 'mouth:open'], 'off': ['mouth:neutral', 'brow:neutral'] + HANDS_OFF},
    'Shadow_Rage': {'on': CB + ['brow:angry', 'mouth:open', 'mouth:fang', 'fx:anger', 'mode:od'],
                    'off': ['mouth:neutral', 'brow:neutral'] + HANDS_OFF},
    'Overdrive': {'on': OD + ['brow:angry', 'mouth:smirk', 'mouth:fang'], 'off': ['mouth:neutral', 'brow:neutral'] + HANDS_OFF},
}
STATES = {
    'NORMAL': {},
    'SHADOW': {'on': SH},
    'COMBAT': {'on': CB + ['brow:angry'], 'off': ['brow:neutral'] + HANDS_OFF},
    'OVERDRIVE': EXPR['Overdrive'],
    'HOOD_UP': {'on': ['hood:up'], 'off': ['hood:down']},
    'HOOD_UP_OVERDRIVE': {'on': OD + ['hood:up', 'brow:angry'], 'off': ['hood:down', 'brow:neutral'] + HANDS_OFF},
}


def sheets(ctx):
    recs, comps, root, comp, flat, sheet = ctx['recs'], ctx['comps'], ctx['root'], ctx['composite'], ctx['flat'], ctx['label_sheet']
    md = os.path.join(root, 'masters')
    os.makedirs(md, exist_ok=True)
    LIGHT_BG, DARK_BG = (236, 238, 242, 255), (28, 30, 36, 255)
    flat(comps['NORMAL'], LIGHT_BG).save(os.path.join(md, 'MSH_HUMAN_FULLBODY_MASTER_v001.png'))
    flat(comps['SHADOW'], DARK_BG).save(os.path.join(md, 'MSH_HUMAN_SHADOW_MASTER_v001.png'))
    flat(comps['COMBAT'], DARK_BG).save(os.path.join(md, 'MSH_HUMAN_COMBAT_MASTER_v001.png'))
    flat(comps['OVERDRIVE'], DARK_BG).save(os.path.join(md, 'MSH_HUMAN_OVERDRIVE_MASTER_v001.png'))
    face_box = (1086, 200, 2086, 1300)
    flat(comps['NORMAL'].crop(face_box), LIGHT_BG).save(os.path.join(md, 'MSH_HUMAN_FACE_MASTER_v001.png'))
    # concepts: A soft/friendly, B core, C spectral/combat (same rig, different direction)
    cA = comp(recs, {'on': ['mouth:smile', 'fx:blush'], 'off': ['mouth:neutral']}, W, H)
    cB = comp(recs, {'on': ['fx:halo']}, W, H)
    cC = comp(recs, {'on': CB + ['hood:up', 'brow:angry', 'fx:halo'], 'off': ['hood:down', 'brow:neutral'] + HANDS_OFF}, W, H)
    for tag, im, bg in (('A', cA, (244, 236, 232, 255)), ('B', cB, LIGHT_BG), ('C', cC, DARK_BG)):
        flat(im, bg).resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(md, f'MSH_HUMAN_CONCEPT_{tag}_v001.png'))
    # turnaround: front + back (built from rig parts: back hair + jacket back brought forward, face parts removed)
    front = comps['NORMAL']
    face_groups = {'08_FACE', '09_EYES', '10_BROWS', '11_MOUTH', '12_FRONT_HAIR', '16_EXPRESSIONS'}
    back_recs = [r for r in recs if r['group'] not in face_groups]
    lift = [r for r in back_recs if r['name'] in ('JacketBack', 'HoodDown', 'Hair_BackMain', 'Hair_BackL', 'Hair_BackR')]
    back_recs = [r for r in back_recs if r not in lift] + lift
    back = comp(back_recs, {}, W, H).transpose(Image.FLIP_LEFT_RIGHT)
    tiles = [('FRONT', front.resize((W // 3, H // 3), Image.LANCZOS)), ('BACK', back.resize((W // 3, H // 3), Image.LANCZOS))]
    sheet(tiles, 2, 'KAGETSU — TURNAROUND (front / back, orthographic)', (24, 26, 32), tile_bg=(214, 218, 226, 255)).save(
        os.path.join(md, 'MSH_HUMAN_TURNAROUND_v001.png'))
    # expressions
    tiles = [(k.replace('_', ' '), comp(recs, v, W, H, face_box).resize((500, 550), Image.LANCZOS)) for k, v in EXPR.items()]
    sheet(tiles, 6, 'KAGETSU — EXPRESSION MASTER (18) — real PSD parts', (24, 26, 32), tile_bg=(214, 218, 226, 255)).save(
        os.path.join(md, 'MSH_HUMAN_EXPRESSION_MASTER_v001.png'))
    # accessories / fx isolated
    names = ['HoodDown', 'HoodUp_Front', 'HoodUp_Peak_L', 'Charm', 'Belt', 'Strap_Hanging', 'Strap_Thigh', 'GloveL',
             'FistR', 'Halo_Crescent_Main', 'Halo_Fragments', 'Wisp01', 'ShadowHandL', 'ShadowFingerL', 'ShadowArm_Rear_L',
             'Fragments01', 'CombatEyeGlowL', 'EyeL_ShadowRing', 'Glitch01', 'Mist_Front', 'Overdrive_Flame_Front',
             'ShadowPool_Large', 'SeamGlow', 'HairGlow_Tip01']
    by = {r['name']: r for r in recs}
    tiles = []
    for n in names:
        t = by[n]['img'].copy()
        t.thumbnail((460, 460))
        tiles.append((n[:22], t))
    sheet(tiles, 6, 'KAGETSU — ACCESSORY / FX MASTER (isolated parts)', (18, 19, 24), tile_bg=(96, 100, 112, 255)).save(
        os.path.join(md, 'MSH_HUMAN_ACCESSORY_MASTER_v001.png'))
    # toggle QA
    tq = [('NORMAL', {}), ('SHADOW (F8)', STATES['SHADOW']), ('COMBAT (Shift+F3)', STATES['COMBAT']),
          ('OVERDRIVE (Shift+F4)', STATES['OVERDRIVE']), ('HOOD (Shift+F2)', STATES['HOOD_UP']),
          ('Hood+Overdrive', STATES['HOOD_UP_OVERDRIVE']),
          ('Halo/Wisps (Ctrl+1)', {'on': ['fx:halo']}), ('Shadow Hands (Ctrl+2)', {'on': ['fx:shadowhands']}),
          ('Eye Glow (Ctrl+3)', {'on': ['fx:eyeglow']}), ('Mist (Ctrl+6)', {'on': ['fx:mist']}),
          ('Glitch (Ctrl+7)', {'on': ['fx:glitch']}), ('Smile (F2)', EXPR['Soft_Smile']), ('Angry (F6)', EXPR['Angry']),
          ('Cry (Shift+F1)', EXPR['Crying'])]
    tiles = [(n, comp(recs, s, W, H).resize((W // 5, H // 5), Image.LANCZOS)) for n, s in tq]
    sheet(tiles, 7, 'Human_Toggle_QA — rendered from real PSD parts', (24, 26, 32), tile_bg=(170, 176, 188, 255)).save(
        os.path.join(root, 'qa', 'Human_Toggle_QA.png'))
