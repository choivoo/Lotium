#!/usr/bin/env python3
"""parts_build.json -> parts_assembly_manifest.json, layer_manifest_final.csv, psd_tree_final.md,
and the half-resolution web-rig parts (12_rig/web)."""
import csv
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
N = ROOT / "08_live2d_notes"
L = sorted(json.loads((N / "parts_build.json").read_text()), key=lambda l: l["z"])
man = {"canvas": {"width": 3072, "height": 4608}, "note": "file paths are relative to this manifest (08_live2d_notes/)",
       "source_masters": ["03_concepts/masters/fullbody/LTM_FULLBODY_MASTER_v001.png",
                          "03_concepts/masters/face/LTM_FACE_MASTER_v001.png",
                          "03_concepts/masters/accessories/LTM_ACCESSORY_MASTER_v001.png",
                          "03_concepts/masters/overclock/LTM_OVERCLOCK_MASTER_v001.png"],
       "layers": [{k: l[k] for k in ("id", "name", "group", "x", "y", "z", "visible", "blend", "toggle", "physics", "param",
                                     "hidden_restored", "source")} | {"file": "../" + l["file"], "w": l["w"], "h": l["h"]}
                  for l in L]}
(N / "parts_assembly_manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
with open(N / "layer_manifest_final.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["layer_id", "layer_name", "group", "file", "x", "y", "width", "height", "z_order", "visible_default",
                "blend", "toggle", "physics", "parameter", "hidden_area_restored", "source"])
    for l in L:
        w.writerow([l["id"], l["name"], l["group"], l["file"], l["x"], l["y"], l["w"], l["h"], l["z"], l["visible"],
                    l["blend"], l["toggle"], l["physics"], l["param"], l["hidden_restored"], l["source"]])
g = OrderedDict()
for l in L:
    g.setdefault(l["group"], []).append(l)
with open(N / "psd_tree_final.md", "w") as f:
    f.write(f"# PSD Tree — LTM_LIVE2D_MASTER_v002.psd\n\n캔버스 3072×4608 · 레이어 {len(L)}개 · 그룹 {len(g)}개 · 위(앞) → 아래(뒤).\n"
            "표기: `[H]` 기본 숨김 · `[+]` Add · `[R]` 가려진 부분 복원/재작화 · `[P]` 물리 · `[T]` 토글\n\n```\nLTM_LIVE2D_MASTER_v002.psd\n")
    for grp in sorted(g, reverse=True):
        f.write(f"├─ {grp}  ({len(g[grp])})\n")
        for l in g[grp]:
            tags = "".join(t for t, c in (("[H]", not l["visible"]), ("[+]", l["blend"] == "add"), ("[R]", l["hidden_restored"]),
                                          ("[P]", l["physics"]), ("[T]", l["toggle"])) if c)
            f.write(f"│   ├─ {l['name']} {tags}\n")
    f.write("```\n")
print("manifests:", len(L))
