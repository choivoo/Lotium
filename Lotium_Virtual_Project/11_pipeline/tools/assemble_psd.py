#!/usr/bin/env python3
"""Assemble Live2D part PNGs into a layered PSD from parts_assembly_manifest.json.

Usage:
    pip install pillow psd-tools
    python3 assemble_psd.py <manifest.json> <out.psd> [--check-only]

Manifest format:
{
  "canvas": {"width": 4000, "height": 6000},
  "layers": [
    {"id": "045", "name": "045_Eye_Iris_L", "group": "05_FACE/Eye_L",
     "file": "08_parts/eyes/045_Eye_Iris_L.png", "x": 0, "y": 0, "z": 45,
     "toggle": false, "physics": false, "param": "ParamEyeBallX", "hidden_restored": false,
     "visible": true, "blend": "normal"}
  ]
}
Paths in "file" are relative to the manifest's directory.
"z": larger = further back (matches layer_list.csv numbering, 001 = frontmost).

Validation (refuses to build fake PSDs):
  - every file exists and is RGBA
  - no fully transparent (empty) layer
  - no two layers with identical pixel data
  - layer fits inside the canvas
"""
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import Group, PixelLayer
from psd_tools.constants import BlendMode


def load(manifest_path):
    manifest_path = Path(manifest_path)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    return manifest_path.parent, data


def validate(base, data):
    errors, hashes, images = [], {}, {}
    cw, ch = data["canvas"]["width"], data["canvas"]["height"]
    for layer in data["layers"]:
        path = base / layer["file"]
        if not path.exists():
            errors.append(f"{layer['name']}: missing file {path}")
            continue
        img = Image.open(path).convert("RGBA")
        if img.getbbox() is None or img.getchannel("A").getbbox() is None:
            errors.append(f"{layer['name']}: empty layer")
        digest = hashlib.sha256(img.tobytes()).hexdigest()
        if digest in hashes:
            errors.append(f"{layer['name']}: identical pixels to {hashes[digest]}")
        hashes[digest] = layer["name"]
        if layer["x"] < 0 or layer["y"] < 0 or layer["x"] + img.width > cw or layer["y"] + img.height > ch:
            errors.append(f"{layer['name']}: outside canvas")
        images[layer["name"]] = img
    return errors, images


def build(data, images, out):
    psd = PSDImage.new("RGBA", (data["canvas"]["width"], data["canvas"]["height"]))
    groups = {}

    def group_for(path):
        if not path:
            return psd
        if path not in groups:
            parent_path, _, name = path.rpartition("/")
            groups[path] = Group.new(group_for(parent_path), name)
        return groups[path]

    # psd-tools appends bottom-to-top, so add the back-most layers first.
    for layer in sorted(data["layers"], key=lambda l: -l["z"]):
        pl = PixelLayer.frompil(images[layer["name"]], group_for(layer.get("group", "")),
                                layer["name"], layer["y"], layer["x"])
        if not layer.get("visible", True):
            pl.visible = False
        if layer.get("blend") == "add":
            pl.blend_mode = BlendMode.LINEAR_DODGE
    psd.save(out)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    base, data = load(sys.argv[1])
    errors, images = validate(base, data)
    for e in errors:
        print("ERROR", e)
    print(f"layers={len(data['layers'])} errors={len(errors)}")
    if errors:
        sys.exit(1)
    if "--check-only" not in sys.argv:
        build(data, images, sys.argv[2])
        print("wrote", sys.argv[2])


if __name__ == "__main__":
    main()
