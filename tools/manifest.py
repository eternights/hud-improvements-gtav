#!/usr/bin/env python3
"""Hash a vanilla scaleform dump into a manifest.

Extract the game's scaleform archives to a directory (same layout every time),
then run:

    python tools/manifest.py vanilla/1.0.3411 -o vanilla/1.0.3411.json

Only .gfx and .ytd files are recorded. Paths are relative to the dump root and
use forward slashes, so manifests compare cleanly across Windows and Linux.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

EXTENSIONS = {".gfx", ".ytd"}


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(root: str) -> dict:
    files = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if os.path.splitext(name)[1].lower() not in EXTENSIONS:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            files[rel] = {"size": os.path.getsize(full), "sha256": sha256(full)}
    return {"files": files}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Hash a vanilla scaleform dump into a manifest."
    )
    parser.add_argument("root", help="directory containing the extracted scaleforms")
    parser.add_argument("-o", "--output", required=True, help="manifest .json to write")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.root):
        parser.error(f"not a directory: {args.root}")

    manifest = build(args.root)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print(f"wrote {len(manifest['files'])} entries to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
