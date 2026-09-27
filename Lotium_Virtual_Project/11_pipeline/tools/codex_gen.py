#!/usr/bin/env python3
"""Generate one image with Codex CLI's built-in image tool.

Usage:
    python3 codex_gen.py <out.png> <prompt_file_or_text> [--ref img.png ...] [--size WxH]

Runs `codex exec` in a scratch dir, asks it to generate the image (passing
reference images with -i for identity consistency) and copy the result to
<out.png>. Never overwrites: exits with an error if <out.png> exists.
Logs every call to 03_concepts/generation_log.csv.
"""
import csv
import datetime
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "03_concepts" / "generation_log.csv"


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    out = Path(args[0]).resolve()
    prompt = Path(args[1]).read_text() if Path(args[1]).is_file() else args[1]
    refs, size = [], "1024x1536"
    rest = args[2:]
    i = 0
    while i < len(rest):
        if rest[i] == "--ref":
            refs.append(str(Path(rest[i + 1]).resolve()))
            i += 2
        elif rest[i] == "--size":
            size = rest[i + 1]
            i += 2
        else:
            i += 1
    if out.exists():
        sys.exit(f"refuse to overwrite {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    ref_note = ("The attached image(s) are the approved master design of this exact character. "
                "Keep the same face, hairstyle, outfit, colors and accessories; only change what the prompt asks.\n"
                if refs else "")
    instruction = (
        "Use your built-in image generation tool (not a script, not an API call) to generate exactly one image. "
        f"Target size {size}. {ref_note}"
        f"Image prompt:\n{prompt}\n\n"
        f"After generation copy the PNG to {out} and print its path. Do nothing else."
    )
    cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "workspace-write", "--add-dir", str(out.parent)]
    for r in refs:
        cmd += ["-i", r]
    cmd.append(instruction)
    with tempfile.TemporaryDirectory() as tmp:
        res = subprocess.run(cmd, cwd=tmp, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=900)
    ok = out.exists()
    new = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp", "file", "refs", "size", "ok", "prompt_head"])
        w.writerow([datetime.datetime.now().isoformat(timespec="seconds"),
                    os.path.relpath(out, ROOT), ";".join(os.path.relpath(r, ROOT) for r in refs),
                    size, ok, prompt[:120].replace("\n", " ")])
    if not ok:
        print(res.stdout[-3000:], res.stderr[-2000:])
        sys.exit("generation failed")
    print("OK", out)


if __name__ == "__main__":
    main()
