"""build_model.py — render parts -> manifest -> previews -> PSD -> reopen QA.

usage: python build_model.py <model_module.py> [--skip-render]

A model module provides:
  MODEL   dict(code, title, W, H, groups, psd, root)
  build_parts() -> [Part]            (bottom -> top z order)
  STATES  {name: {'on': [...], 'off': [...]}}
  derived(rendered) -> [(Part, img, x, y)]   optional (silhouette glows etc.)
  sheets(ctx)                         optional (expression / FX / toggle sheets)
"""
import csv, hashlib, importlib.util, json, os, sys, time
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from partkit import blend_over, to_image  # noqa: E402

FONT = None


def font(sz):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
              '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'):
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def load(path):
    spec = importlib.util.spec_from_file_location('model', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _render(args):
    p, W, H = args
    img, x, y = p.render(W, H)
    return img, x, y


# ------------------------------------------------------------------ state logic
def visible_in(rec, state):
    on, off = state.get('on', []), state.get('off', [])
    tags = [t for t in rec['toggle'].split('|') if t] + [rec['name']]
    if any(t in off for t in tags):
        return False
    if rec['visible']:
        return True
    return any(t in on for t in tags)


def composite(recs, state, W, H, box=None):
    base = np.zeros((H, W, 4), np.float32)
    for r in recs:
        if visible_in(r, state):
            if '_f' not in r:
                r['_f'] = np.asarray(r['img'], np.float32) / 255.0
            blend_over(base, r['_f'], r['x'], r['y'], r['blend'])
    im = to_image(base)
    return im.crop(box) if box else im


def flat(im, bg):
    out = Image.new('RGBA', im.size, bg)
    out.alpha_composite(im)
    return out.convert('RGB')


def label_sheet(tiles, cols, title, bg, tile_bg=None, scale=1.0):
    """tiles: [(label, RGBA image)] -> labelled grid"""
    tw = max(t[1].width for t in tiles)
    th = max(t[1].height for t in tiles)
    tw, th = int(tw * scale), int(th * scale)
    rows = (len(tiles) + cols - 1) // cols
    pad, lab = 24, 56
    sheet = Image.new('RGB', (cols * (tw + pad) + pad, 110 + rows * (th + lab + pad) + pad), bg)
    d = ImageDraw.Draw(sheet)
    d.text((pad, 30), title, fill=(230, 235, 240), font=font(44))
    for i, (name, im) in enumerate(tiles):
        c, r = i % cols, i // cols
        x, y = pad + c * (tw + pad), 110 + r * (th + lab + pad)
        im2 = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        tile = Image.new('RGBA', (tw, th), tile_bg or (58, 60, 68, 255))
        tile.alpha_composite(im2, ((tw - im2.width) // 2, (th - im2.height) // 2))
        sheet.paste(tile.convert('RGB'), (x, y + lab))
        d.text((x + 4, y + 8), name, fill=(170, 255, 215), font=font(34))
    return sheet


# ------------------------------------------------------------------ main
def main(model_path, skip_render=False):
    t0 = time.time()
    M = load(model_path)
    cfg = M.MODEL
    W, H, root = cfg['W'], cfg['H'], cfg['root']
    parts = M.build_parts()
    order = {g: i for i, g in enumerate(cfg['groups'])}
    for p in parts:
        assert p.group in order, (p.name, p.group)
    names = [p.name for p in parts]
    dup = {n for n in names if names.count(n) > 1}
    assert not dup, dup
    parts = sorted(parts, key=lambda p: order[p.group])  # stable: z inside group kept

    print(f'[{cfg["code"]}] rendering {len(parts)} parts @ {W}x{H}')
    with Pool(os.cpu_count()) as pool:
        out = pool.map(_render, [(p, W, H) for p in parts], chunksize=1)
    recs = []
    for p, (img, x, y) in zip(parts, out):
        recs.append(dict(name=p.name, group=p.group, blend=p.blend, visible=p.visible, toggle=p.toggle,
                         physics=p.physics, param=p.param, restore=p.restore, note=p.note, img=img, x=x, y=y))
    if hasattr(M, 'derived'):
        extra = M.derived(recs, W, H)
        for p, img, x, y in extra:
            rec = dict(name=p.name, group=p.group, blend=p.blend, visible=p.visible, toggle=p.toggle,
                       physics=p.physics, param=p.param, restore=p.restore, note=p.note, img=img, x=x, y=y)
            # insert at end of its group
            gi = order[p.group]
            idx = max([i for i, r in enumerate(recs) if order[r['group']] <= gi], default=-1) + 1
            recs.insert(idx, rec)
    empty = [r['name'] for r in recs if r['img'] is None]
    assert not empty, f'empty parts: {empty}'
    print(f'  rendered in {time.time() - t0:.1f}s')

    # ---------------------------------------------------------------- PNGs + manifest
    pdir = os.path.join(root, 'parts')
    for f in os.listdir(pdir) if os.path.isdir(pdir) else []:
        import shutil
        shutil.rmtree(os.path.join(pdir, f)) if os.path.isdir(os.path.join(pdir, f)) else os.remove(os.path.join(pdir, f))
    rows = []
    for z, r in enumerate(recs, 1):
        gdir = os.path.join(pdir, r['group'])
        os.makedirs(gdir, exist_ok=True)
        fn = f'{cfg["code"]}_{z:03d}_{r["name"]}.png'
        r['png'] = os.path.join('parts', r['group'], fn)
        r['img'].save(os.path.join(root, r['png']), optimize=False, compress_level=6)
        r['id'] = f'{cfg["code"]}_{z:03d}'
        r['z'] = z
        rows.append({'ID': r['id'], 'Name': r['name'], 'Group': r['group'], 'PNG File': r['png'],
                     'X': r['x'], 'Y': r['y'], 'Width': r['img'].width, 'Height': r['img'].height,
                     'Z-order': z, 'Blend mode': r['blend'], 'Default visibility': 'ON' if r['visible'] else 'OFF',
                     'Toggle': r['toggle'], 'Physics': r['physics'], 'Live2D parameter': r['param'],
                     'Hidden restoration': r['restore'], 'Note': r['note']})
    with open(os.path.join(root, 'layer_manifest_final.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(root, 'parts_assembly_manifest.json'), 'w') as f:
        json.dump({'model': cfg['code'], 'title': cfg['title'], 'canvas': [W, H], 'psd': cfg['psd'],
                   'groups_bottom_to_top': cfg['groups'], 'layers_bottom_to_top': rows}, f, indent=1)
    tree = [f'# PSD tree — {cfg["psd"]}', '', f'Canvas {W}×{H}, RGBA 8-bit. Listed top → bottom (as in Photoshop).', '']
    for g in reversed(cfg['groups']):
        members = [r for r in recs if r['group'] == g]
        if not members:
            continue
        tree.append(f'- 📁 **{g}** ({len(members)})')
        for r in reversed(members):
            flags = []
            if not r['visible']:
                flags.append('hidden')
            if r['blend'] != 'normal':
                flags.append(r['blend'])
            if r['toggle']:
                flags.append('toggle=' + r['toggle'])
            tree.append(f'  - `{r["id"]}` {r["name"]}' + (f'  _({", ".join(flags)})_' if flags else ''))
    open(os.path.join(root, 'psd_tree_final.md'), 'w').write('\n'.join(tree) + '\n')

    # ---------------------------------------------------------------- state previews
    qdir = os.path.join(root, 'qa')
    os.makedirs(os.path.join(qdir, 'previews'), exist_ok=True)
    comps = {}
    for sname, st in M.STATES.items():
        im = composite(recs, st, W, H)
        comps[sname] = im
        flat(im, cfg.get('bg', (236, 238, 242, 255))).resize((W // 2, H // 2), Image.LANCZOS).save(
            os.path.join(qdir, 'previews', f'{cfg["code"]}_{sname}.png'))
    ctx = dict(recs=recs, comps=comps, W=W, H=H, root=root, composite=composite, flat=flat,
               label_sheet=label_sheet, font=font, visible_in=visible_in)
    if hasattr(M, 'sheets'):
        M.sheets(ctx)
    print(f'  previews/sheets done {time.time() - t0:.1f}s')

    # ---------------------------------------------------------------- PSD
    from assemble_psd import assemble, verify
    psd_path = os.path.join(root, 'psd', cfg['psd'])
    assemble(recs, cfg, psd_path)
    qa = verify(recs, cfg, psd_path, comps[cfg['default_state']], root)
    print(f'  PSD + QA done {time.time() - t0:.1f}s  -> {qa["summary"]}')
    return qa


if __name__ == '__main__':
    main(sys.argv[1])
