"""assemble_psd.py — grouped PSD writer + independent reopen verification / anti-fake QA."""
import hashlib, json, os
import numpy as np
from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer, Group
from psd_tools.constants import BlendMode, Compression

BLEND = {'normal': BlendMode.NORMAL, 'add': BlendMode.LINEAR_DODGE,
         'screen': BlendMode.SCREEN, 'multiply': BlendMode.MULTIPLY}
BLEND_BACK = {v: k for k, v in BLEND.items()}


def assemble(recs, cfg, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    psd = PSDImage.new('RGBA', (cfg['W'], cfg['H']))
    groups = {}
    for g in cfg['groups']:  # bottom -> top
        if any(r['group'] == g for r in recs):
            groups[g] = Group.new(psd, name=g)
    for r in recs:
        lyr = PixelLayer.frompil(r['img'], psd, r['name'], r['y'], r['x'], Compression.RLE)
        lyr.blend_mode = BLEND[r['blend']]
        lyr.visible = bool(r['visible'])
        groups[r['group']].append(lyr)
    if 'guide_hidden_groups' in cfg:
        for g in cfg['guide_hidden_groups']:
            if g in groups:
                groups[g].visible = False
    psd.save(path)


def _grad_energy(im, box):
    a = np.asarray(im.crop(box).convert('L'), np.float32)
    gx = np.abs(np.diff(a, axis=1)).mean()
    gy = np.abs(np.diff(a, axis=0)).mean()
    return float(gx + gy)


def verify(recs, cfg, path, default_comp, root):
    res = {'checks': [], 'warn': [], 'fail': []}

    def check(name, ok, detail='', level='FAIL'):
        res['checks'].append({'check': name, 'result': 'PASS' if ok else level, 'detail': detail})
        if not ok:
            res['fail' if level == 'FAIL' else 'warn'].append(f'{name}: {detail}')

    W, H = cfg['W'], cfg['H']
    # ---- anti-fake on source parts
    empty = [r['name'] for r in recs if np.asarray(r['img'])[..., 3].max() <= 2]
    check('empty layers = 0', not empty, f'{len(empty)} {empty[:5]}')
    fake = [r['name'] for r in recs if (np.asarray(r['img'])[..., 3] > 16).sum() < 60]
    check('fake transparent layers = 0', not fake, f'{len(fake)} {fake[:5]}')
    hashes = {}
    for r in recs:
        h = hashlib.sha1(r['img'].tobytes() + bytes(str(r['img'].size), 'ascii')).hexdigest()
        hashes.setdefault(h, []).append(r['name'])
    dups = [v for v in hashes.values() if len(v) > 1]
    check('exact duplicate layers = 0', not dups, str(dups[:5]))
    oob = [r['name'] for r in recs if r['x'] < 0 or r['y'] < 0 or r['x'] + r['img'].width > W or r['y'] + r['img'].height > H]
    check('unexpected canvas offsets = 0', not oob, str(oob[:5]))
    wrong = [r['name'] for r in recs if r['img'].width > W or r['img'].height > H or r['img'].mode != 'RGBA']
    check('wrong-size parts = 0', not wrong, str(wrong[:5]))
    missing = [r['png'] for r in recs if not os.path.exists(os.path.join(root, r['png']))]
    check('manifest missing file = 0', not missing, str(missing[:5]))

    # ---- independent reopen
    try:
        psd = PSDImage.open(path)
        err = None
    except Exception as e:  # pragma: no cover
        err = repr(e)
    check('PSD reopen errors = 0', err is None, str(err))
    if err:
        return _write(res, cfg, root, {})
    check('canvas size', psd.size == (W, H), f'{psd.size}')
    top_groups = [g.name for g in psd]  # bottom -> top
    exp_groups = [g for g in cfg['groups'] if any(r['group'] == g for r in recs)]
    check('group order', top_groups == exp_groups, f'{top_groups}')
    layers = [l for l in psd.descendants() if l.kind == 'pixel']
    check('layer count matches manifest', len(layers) == len(recs), f'{len(layers)} vs {len(recs)}')
    mism = []
    for l, r in zip(layers, recs):
        probs = []
        if l.name != r['name']:
            probs.append('name')
        if l.parent.name != r['group']:
            probs.append('group')
        if BLEND_BACK.get(l.blend_mode) != r['blend']:
            probs.append('blend')
        if bool(l.visible) != bool(r['visible']):
            probs.append('visible')
        if (l.left, l.top) != (r['x'], r['y']):
            probs.append('offset')
        a = np.asarray(l.topil().convert('RGBA'))
        b = np.asarray(r['img'])
        if a.shape != b.shape or not np.array_equal(a[..., 3], b[..., 3]) or \
                np.abs(a[..., :3].astype(int) - b[..., :3].astype(int))[b[..., 3] > 0].max(initial=0) > 1:
            probs.append('pixels')
        if probs:
            mism.append((r['name'], probs))
    check('reopened layer name/group/Z-order/blend/visibility/offset/pixels', not mism, str(mism[:6]))

    # ---- composite of reopened PSD vs pipeline default composite (== Fullbody Master)
    pc = psd.composite(force=True)
    pc = pc.convert('RGBA') if pc is not None else Image.new('RGBA', (W, H))
    a = np.asarray(pc, np.float32) / 255
    b = np.asarray(default_comp, np.float32) / 255
    pa = a[..., :3] * a[..., 3:4]
    pb = b[..., :3] * b[..., 3:4]
    mad = float(np.abs(pa - pb).mean() * 255)
    p99 = float(np.percentile(np.abs(pa - pb).max(axis=2) * 255, 99.9))
    check('reopened PSD composite == Fullbody Master', mad < 1.0 and p99 < 12, f'mean abs diff {mad:.3f}/255, p99.9 {p99:.1f}')
    flat = Image.new('RGBA', (W, H), (236, 238, 242, 255))
    flat.alpha_composite(pc)
    flat.convert('RGB').resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(root, 'qa', f'{cfg["code"]}_PSD_REOPEN_COMPOSITE.png'))

    # ---- hidden-area restoration: how much of each restored part is covered in default pose
    cover = np.zeros((H, W), np.float32)
    stats = {}
    for r in reversed(recs):
        if not r['visible'] or r['blend'] != 'normal':
            continue
        al = np.asarray(r['img'])[..., 3].astype(np.float32) / 255
        x, y = r['x'], r['y']
        h, w = al.shape
        sub = cover[y:y + h, x:x + w]
        if r['restore']:
            solid = al > 0.5
            hid = (solid & (sub > 0.97)).sum()
            stats[r['name']] = dict(restore=r['restore'], solid_px=int(solid.sum()), hidden_px=int(hid),
                                    hidden_pct=round(100 * hid / max(solid.sum(), 1), 1))
        sub[:] = 1 - (1 - sub) * (1 - al)
    no_hidden = [k for k, v in stats.items() if v['hidden_px'] < 50]
    check('restored parts have real hidden area', not no_hidden, str(no_hidden[:5]), level='WARN')
    check('hidden-area restoration count', len(stats) >= cfg.get('min_restore', 5), f'{len(stats)} restored parts')

    # ---- sharpness parity face vs body (Lotium body-blur regression guard)
    fe = _grad_energy(default_comp, cfg['face_box'])
    be = _grad_energy(default_comp, cfg['body_box'])
    ratio = be / max(fe, 1e-6)
    check('face/body sharpness parity (native-res parts, no upscale)', ratio > 0.35, f'body/face edge energy {ratio:.2f}', level='WARN')
    # alpha edge quality: premultiplied halo check (bright fringe on dark parts)
    halo = []
    for r in recs:
        arr = np.asarray(r['img']).astype(np.int32)
        edge = (arr[..., 3] > 8) & (arr[..., 3] < 120)
        if edge.sum() > 50 and r['blend'] == 'normal':
            core = arr[..., 3] > 250
            if core.sum() > 50:
                le = arr[..., :3][edge].mean()
                lc = arr[..., :3][core].mean()
                if le > 200 and le - lc > 90:
                    halo.append(r['name'])
    check('anti-alias edges (no white halo)', not halo, str(halo[:5]), level='WARN')

    extra = dict(layers=len(recs), groups=len(exp_groups), hidden_layers=sum(1 for r in recs if not r['visible']),
                 add_screen=sum(1 for r in recs if r['blend'] in ('add', 'screen')),
                 multiply=sum(1 for r in recs if r['blend'] == 'multiply'),
                 restored_parts=len(stats), restore_stats=stats,
                 psd_bytes=os.path.getsize(path), psd=path)
    return _write(res, cfg, root, extra)


def _write(res, cfg, root, extra):
    npass = sum(1 for c in res['checks'] if c['result'] == 'PASS')
    res['summary'] = f'PASS {npass} / WARN {len(res["warn"])} / FAIL {len(res["fail"])}'
    res.update(extra)
    json.dump(res, open(os.path.join(root, 'qa', f'{cfg["code"]}_psd_qa.json'), 'w'), indent=1)
    md = [f'# PSD QA — {cfg["psd"]}', '', f'**{res["summary"]}**', '', '| Check | Result | Detail |', '|---|---|---|']
    md += [f'| {c["check"]} | {c["result"]} | {c["detail"]} |' for c in res['checks']]
    if extra:
        md += ['', f'- Layers: {extra["layers"]}  · Groups: {extra["groups"]}  · Hidden by default: {extra["hidden_layers"]}',
               f'- Add/Screen FX: {extra["add_screen"]}  · Multiply: {extra["multiply"]}',
               f'- PSD size: {extra["psd_bytes"] / 1e6:.1f} MB', '', '## Hidden-area restoration', '',
               '| Part | Restored region | Solid px | Hidden in default pose |', '|---|---|---|---|']
        md += [f'| {k} | {v["restore"]} | {v["solid_px"]} | {v["hidden_pct"]}% |' for k, v in extra['restore_stats'].items()]
    open(os.path.join(root, 'qa', f'{cfg["code"]}_psd_qa.md'), 'w').write('\n'.join(md) + '\n')
    return res
