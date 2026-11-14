#!/usr/bin/env python3
"""Compare two vanilla manifests and report what a game update touched.

    python tools/compare.py vanilla/1.0.3411.json vanilla/1.0.3551.json

Pass --src to mark files you patch and get a "needs re-applying" list:

    python tools/compare.py old.json new.json --src "src/*/patch.json"

The glob is expanded by the shell on Linux/macOS; on Windows quote it and let
Python expand it (it accepts both: a single file or a glob pattern).
"""

from __future__ import annotations

import argparse
import glob
import json
import sys


def load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)["files"]


def load_targets(pattern: str) -> dict:
    paths = glob.glob(pattern) or [pattern]
    targets = {}
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        targets[data["target"]] = data
    return targets


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare two vanilla scaleform manifests."
    )
    parser.add_argument("old", help="manifest of the previous build")
    parser.add_argument("new", help="manifest of the new build")
    parser.add_argument(
        "--src",
        metavar="GLOB",
        help="patch.json files to mark, e.g. src/*/patch.json",
    )
    args = parser.parse_args(argv)

    old = load_manifest(args.old)
    new = load_manifest(args.new)
    targets = load_targets(args.src) if args.src else {}

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(
        path
        for path in set(old) & set(new)
        if old[path].get("sha256") != new[path].get("sha256")
    )

    for label, group in (("ADDED", added), ("REMOVED", removed), ("CHANGED", changed)):
        for path in group:
            mark = "  <- patched" if path in targets else ""
            print(f"{label:7} {path}{mark}")

    print(f"\n{len(added)} added, {len(removed)} removed, {len(changed)} changed")

    if targets:
        stale = [path for path in targets if path in set(added) | set(removed) | set(changed)]
        files_word = "file" if len(targets) == 1 else "files"
        need_word = "needs" if len(stale) == 1 else "need"
        print(
            f"{len(targets)} patched {files_word}; "
            f"{len(stale)} {need_word} re-applying this update"
        )
        for path in stale:
            print(f"  reopen {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
