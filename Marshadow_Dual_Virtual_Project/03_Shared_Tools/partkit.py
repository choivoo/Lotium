"""partkit — procedural Live2D part engine (shared by Mini + Human models).

Every part is authored as a stack of vector ops (smooth fills, clipped shading,
strokes, erasers, blurred glows), rendered supersampled into its own cropped
RGBA image with a canvas offset.  Because each part is drawn as a complete
shape, the regions normally hidden behind other parts are restored by design
(hidden-area restoration), and the composite of all default-visible parts is
the Fullbody Master.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops


# ----------------------------------------------------------------- geometry
def catmull(pts, closed=True, n=10):
    """Catmull-Rom spline through pts -> dense polyline."""
    pts = [tuple(map(float, p)) for p in pts]
    if len(pts) < 3:
        return pts
    out = []
    m = len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0 = pts[(i - 1) % m] if closed or i > 0 else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % m]
        p3 = pts[(i + 2) % m] if closed or i + 2 < m else pts[-1]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(pts[-1])
    return out


def ellipse_pts(cx, cy, rx, ry, rot=0.0, n=72):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(cx + rx * math.cos(a) * c - ry * math.sin(a) * s,
             cy + rx * math.cos(a) * s + ry * math.sin(a) * c)
            for a in (2 * math.pi * i / n for i in range(n))]


def arc_pts(cx, cy, rx, ry, a0, a1, n=48):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1)))) for i in range(n)]


def mirror(pts, cx):
    return [(2 * cx - x, y) for x, y in pts]


def shift(pts, dx=0, dy=0):
    return [(x + dx, y + dy) for x, y in pts]


def scale(pts, sx, sy=None, ox=0, oy=0):
    sy = sx if sy is None else sy
    return [(ox + (x - ox) * sx, oy + (y - oy) * sy) for x, y in pts]


def band(path, w0, w1=None, n=10):
    """Closed ribbon polygon around an open smooth path with width w0 -> w1 (tapered)."""
    w1 = w0 if w1 is None else w1
    p = catmull(path, closed=False, n=n)
    L, R = [], []
    for i, (x, y) in enumerate(p):
        a = p[max(i - 1, 0)]
        b = p[min(i + 1, len(p) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        t = i / (len(p) - 1)
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy / d * w, y + dx / d * w))
        R.append((x + dy / d * w, y - dx / d * w))
    return L + R[::-1]


# ----------------------------------------------------------------- colours
def hexc(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


# ----------------------------------------------------------------- part
class Part:
    def __init__(self, name, group, blend='normal', visible=True, toggle='', physics='',
                 param='', restore='', note='', opacity=1.0):
        self.name, self.group, self.blend, self.visible = name, group, blend, visible
        self.toggle, self.physics, self.param, self.restore, self.note = toggle, physics, param, restore, note
        self.opacity = opacity
        self.ops = []
        self.post_blur = 0

    # authoring API -------------------------------------------------------
    def fill(self, pts, color, smooth=True, outline=None, ow=0, blur=0):
        self.ops.append(('fill', pts, color, smooth, blur))
        if outline is not None and ow:
            self.ops.append(('stroke', pts, outline, ow, True, smooth, False, 0))
        return self

    def shade(self, pts, color, smooth=True, blur=0):
        """fill clipped to what the part already contains"""
        self.ops.append(('shade', pts, color, smooth, blur))
        return self

    def stroke(self, pts, color, w, closed=False, smooth=True, clip=False, blur=0):
        self.ops.append(('stroke', pts, color, w, closed, smooth, clip, blur))
        return self

    def erase(self, pts, smooth=True, blur=0):
        self.ops.append(('erase', pts, None, smooth, blur))
        return self

    def clip(self, pts, smooth=True):
        """keep only what lies inside pts (applied at this point of the stack)"""
        self.ops.append(('clip', pts, None, smooth, 0))
        return self

    def glow(self, pts, color, blur, smooth=True):
        self.ops.append(('fill', pts, color, smooth, blur))
        return self

    # rendering -------------------------------------------------------------
    def _bbox(self):
        xs, ys, m = [], [], 4
        for op in self.ops:
            pts = op[1]
            xs += [p[0] for p in pts]
            ys += [p[1] for p in pts]
            if op[0] == 'stroke':
                m = max(m, op[3] + 4 + op[7] * 3)
            else:
                m = max(m, op[4] * 3 + 4)
        m += self.post_blur * 3
        return int(min(xs) - m), int(min(ys) - m), int(max(xs) + m) + 1, int(max(ys) + m) + 1

    def render(self, W, H):
        x0, y0, x1, y1 = self._bbox()
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
        w, h = x1 - x0, y1 - y0
        ss = 3 if w * h < 1_600_000 else 2
        S = (w * ss, h * ss)
        layer = Image.new('RGBA', S, (0, 0, 0, 0))

        def tr(pts, smooth, closed=True):
            p = catmull(pts, closed=closed) if smooth and len(pts) > 2 else pts
            return [((x - x0) * ss, (y - y0) * ss) for x, y in p]

        def blurred(mask, b):
            if not b:
                return mask
            small = mask.resize((w, h), Image.BOX).filter(ImageFilter.GaussianBlur(b))
            return small.resize(S, Image.BILINEAR)

        for op in self.ops:
            kind = op[0]
            mask = Image.new('L', S, 0)
            d = ImageDraw.Draw(mask)
            if kind in ('fill', 'shade', 'erase', 'clip'):
                _, pts, color, smooth, b = op
                d.polygon(tr(pts, smooth), fill=255)
                mask = blurred(mask, b)
            else:
                _, pts, color, wd, closed, smooth, clip, b = op
                p = tr(pts, smooth, closed)
                if closed:
                    p = p + [p[0], p[1]]
                d.line(p, fill=255, width=max(1, int(wd * ss)), joint='curve')
                r = wd * ss / 2
                if not closed:
                    for q in (p[0], p[-1]):
                        d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=255)
                mask = blurred(mask, b)
                if clip:
                    mask = ImageChops.multiply(mask, layer.getchannel('A'))
            if kind == 'shade':
                mask = ImageChops.multiply(mask, layer.getchannel('A'))
            if kind == 'clip':
                layer.putalpha(ImageChops.multiply(layer.getchannel('A'), mask))
                continue
            if kind == 'erase':
                a = ImageChops.subtract(layer.getchannel('A'), mask)
                layer.putalpha(a)
                continue
            src = self._color_img(color, S, x0, y0, ss)
            ca = src.getchannel('A')
            src.putalpha(ImageChops.multiply(mask, ca))
            layer = Image.alpha_composite(layer, src)

        img = layer.convert('RGBa').resize((w, h), Image.LANCZOS).convert('RGBA')
        if self.post_blur:
            img = img.convert('RGBa').filter(ImageFilter.GaussianBlur(self.post_blur)).convert('RGBA')
        if self.opacity < 1:
            img.putalpha(img.getchannel('A').point(lambda v: int(v * self.opacity)))
        bb = img.getchannel('A').point(lambda v: 255 if v > 2 else 0).getbbox()
        if bb is None:
            return None, 0, 0
        return img.crop(bb), x0 + bb[0], y0 + bb[1]

    @staticmethod
    def _color_img(color, S, x0, y0, ss):
        if isinstance(color, tuple) and len(color) == 4 and isinstance(color[0], int):
            return Image.new('RGBA', S, color)
        kind = color[0]
        H, W = S[1], S[0]
        if kind == 'v':  # ('v', c_top, c_bot, y_top, y_bot)  global coords
            _, c1, c2, ya, yb = color
            ys = (np.arange(H) / ss + y0 - ya) / max(yb - ya, 1)
            t = np.clip(ys, 0, 1)[:, None, None]
            arr = (np.array(c1)[None, None] * (1 - t) + np.array(c2)[None, None] * t)
            arr = np.broadcast_to(arr, (H, W, 4))
        elif kind == 'r':  # ('r', c_in, c_out, cx, cy, r)
            _, c1, c2, cx, cy, r = color
            xs = np.arange(W) / ss + x0 - cx
            ys = np.arange(H) / ss + y0 - cy
            t = np.clip(np.sqrt(xs[None, :] ** 2 + ys[:, None] ** 2) / r, 0, 1)[..., None]
            arr = np.array(c1)[None, None] * (1 - t) + np.array(c2)[None, None] * t
        else:
            raise ValueError(color)
        return Image.fromarray(np.ascontiguousarray(arr).astype(np.uint8), 'RGBA')


# ----------------------------------------------------------------- compositing
def blend_over(base, img, x, y, mode='normal'):
    """base: float32 HxWx4 straight-alpha 0..1 array (in place)."""
    a = img if isinstance(img, np.ndarray) else np.asarray(img, dtype=np.float32) / 255.0
    h, w = a.shape[:2]
    H, W = base.shape[:2]
    xa, ya, xb, yb = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if xa >= xb or ya >= yb:
        return
    s = a[ya - y:yb - y, xa - x:xb - x]
    b = base[ya:yb, xa:xb]
    cs, as_ = s[..., :3], s[..., 3:4]
    cb, ab = b[..., :3], b[..., 3:4]
    if mode == 'normal':
        B = cs
    elif mode == 'add':
        B = np.minimum(cb + cs, 1)
    elif mode == 'screen':
        B = cb + cs - cb * cs
    elif mode == 'multiply':
        B = cb * cs
    else:
        raise ValueError(mode)
    ao = as_ + ab * (1 - as_)
    co = cs * as_ * (1 - ab) + cb * ab * (1 - as_) + as_ * ab * B
    b[..., :3] = np.where(ao > 0, co / np.maximum(ao, 1e-6), 0)
    b[..., 3:4] = ao


def to_image(base, bg=None):
    im = Image.fromarray((np.clip(base, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGBA')
    if bg is not None:
        out = Image.new('RGBA', im.size, bg)
        out.alpha_composite(im)
        return out.convert('RGB')
    return im
