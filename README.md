# HUD Improvements — GTA V Enhanced

Scaleform replacements for the GTA V Enhanced HUD and loading screens: the 2013
loading/saving ring artwork, plus the HUD edits kept in this repo.

See [docs/scaleforms-reference.md](docs/scaleforms-reference.md) for what each
`.gfx` in the game does and where the loading rings live.

## What ships

`mod/` is a drop-in tree that mirrors the game's archive layout exactly:

```text
mod/update/update.rpf/x64/data/cdimages/scaleform_frontend.rpf/loadingscreen_startup.gfx
mod/update/update.rpf/x64/data/cdimages/scaleform_generic.rpf/hud_saving.gfx
```

Install with OpenIV: enable **Edit mode**, then copy the contents of `mod/` into
a `mods/` folder in the game directory (or package `mod/` as an `.oiv`). No other
files are touched.

## Repo layout

| Path | Purpose |
| --- | --- |
| `mod/` | The shipped files, byte-for-byte, already in game paths. |
| `src/` | One `patch.json` per modded file: the vanilla hash it was built from plus every change made. This is what makes updates re-appliable instead of guesswork. |
| `vanilla/` | Hash manifests of vanilla scaleform dumps (`*.json` only — the dumps themselves are gitignored). |
| `tools/` | `manifest.py` (hash a dump) and `compare.py` (what changed between builds). |
| `docs/` | Reference material. |

Why binaries live in `mod/` instead of diffs: `.gfx` files cannot be three-way
merged, so the shipped artifact is the full file. `patch.json` is the audit
record — it says *which* tag or texture was changed, so the same edit can be
replayed onto a new vanilla file by hand in minutes.

## Updating for a new game build

The old routine was "find which gfx changed, then redo every edit from vanilla".
With hashes and recipes it becomes:

1. Extract the new vanilla scaleforms to `vanilla/<build>/`, using the **same
   top-level layout every time** (e.g. `update/update.rpf/x64/data/cdimages/...`,
   and `x64b.rpf/data/cdimages/...` if you track the base copies). Paths inside
   the manifest are relative to that root, so they stay stable across builds.
   This directory is gitignored.
2. Build the manifest:

   ```bash
   python tools/manifest.py vanilla/<build> -o vanilla/<build>.json
   ```

3. Compare against the previous build, marking your own files:

   ```bash
   python tools/compare.py vanilla/<old>.json vanilla/<build>.json --src "src/*/patch.json"
   ```

   Output lists `ADDED` / `REMOVED` / `CHANGED` files and appends
   `<- patched` to anything you modify, then prints how many of your patches
   need attention this update.

4. For every file **not** listed: its vanilla bytes are unchanged, so copy your
   existing `mod/` file forward as-is. For every file listed: open its
   `src/<name>/patch.json`, replay just those changes onto the new vanilla file,
   and update `vanilla_build` / `base_sha256`.

5. Tag the release (`git tag v<build>`) and attach a zip of `mod/` plus a short
   changelog to the GitHub release.

`main` always targets the newest game build. If you want to keep supporting an
older build, branch from the matching tag (`legacy-<build>`) instead of trying
to keep one tree compatible with several.

## Automation ceiling

- **Texture-only changes** (most HUD art) can be replayed by a script: ffdec's
  CLI can replace images in a `.gfx` without touching tags.
- **Tag-level changes** (adding a `DefineExternalImage2`, repointing a bitmap
  fill) are not scriptable with stock ffdec; replay them by hand from
  `patch.json`. `tools/apply.py` can be added later if the list of tag edits
  grows.

## Large files

`.gfx`, `.ytd` and `.dds` are committed as plain binaries (marked binary in
`.gitattributes`, no LFS), because the files already tracked in this repo were
added that way. Keep extracted vanilla dumps and `dist/` out of git; only the
manifests belong in `vanilla/`.

## Credits

Vanilla scaleform boundaries and script behaviour documented from
`eternights/decompiled-scaleforms-gtav` and `floppystudiodev/GTAV-Scaleforms-Decompiled`.
