# Agent notes — HUD Improvements (GTA V Enhanced)

Read this before touching the repo. It exists so a fresh chat does not have to
rediscover the project or the scaleform layout.

## What this repo is

Scaleform replacements for the GTA V Enhanced HUD and loading screens: the 2013
loading/saving ring artwork, minimap/cursor work, and the rest of the HUD edits.

- `mod/` — the shipped files, byte-for-byte, in game paths. This is what users install.
- `src/<gfx>/patch.json` — every change made to that file, plus the vanilla hash it was built from.
- `vanilla/<build>.json` — hash manifests of vanilla dumps (no game files in git).
- `tools/manifest.py`, `tools/compare.py` — build manifests / see what a game update changed.
- `docs/scaleforms-reference.md` — what each of the 182 `.gfx` does, the loading-ring
  sites, and the image-naming rules. Read it before editing a scaleform.

## The scaleform decompiles are not in this repo

They are a separate public repo: `eternights/decompiled-scaleforms-gtav`
(182 `.gfx`, 4,269 `.as` files, textures excluded). Any chat can fetch a
scripts-only sparse clone — no authentication, no game install:

```bash
bash tools/fetch-scaleforms.sh          # -> _scaleforms/ (gitignored, ~52 MB)
```

Do not commit `_scaleforms/`. If the clone is missing, run the script instead of
guessing at scaleform internals.

## Paths that matter

All under `update/update.rpf/x64/data/cdimages/` unless noted:

| Scaleform | Archive |
| --- | --- |
| `loadingscreen_startup` | `scaleform_frontend.rpf` |
| `hud_saving`, `saving_footer`, `instructional_buttons` | `scaleform_generic.rpf` |
| `minimap`, `minimap_main_map` | `scaleform_minimap.rpf` (patch paths use `x64/patch/...`) |

The Enhanced game loads `update.rpf`; the same-named file under `x64b.rpf` is
shadowed, so edits there do nothing.

## Facts that have already cost time

- **Loading rings** render in `hud_saving` (`CONTENT.dialogMC.iconMC.spinnerMC`,
  sprite 16, 60 frames), `saving_footer` (`spinnerMC`, 59 frames),
  `loadingscreen_startup` (`LEGALSCREEN.spinner` / `.loading` / `.scstar`), and
  the instructional-buttons family (`button_50`, 59 frames).
- **External images resolve by name, not by ID.** `loadingscreen_startup`'s image
  table is `1 orange_grad`, `2 loadingscreen_startup_i85`, `3 GTAV_SavingSpinner_g`,
  `4 GTAV_SavingSpinner_IB`, `5 beach_fg`, `6 beach_bg`. A new
  `DefineExternalImage2` needs `exportName`/`fileName` set to the texture name;
  an unnamed tag falls back to `<gfx>_i<id>` and renders white.
- **Blips**: the order of `getListOfBlips()` in
  `minimap.gfx/scripts/.../constants/Blips.as` is the sprite ID. `radar_police_ped`
  = 3, `radar_police` = 41, `radar_police_chase` = 42, `radar_police_heli` = 43.
  Which sprite a blip uses is chosen by the game/script, not by the GFX; a
  `SetBlipSprite` change needs a script, and engine-owned wanted blips cannot be
  retargeted at all. Editing the GFX only changes what each ID looks like.
- **The radar map, GPS line and player arrow are engine-rendered**, not movie
  symbols. `minimap.gfx` contains no stealth/dark-arrow logic (its scripts only
  handle health/armour, wanted stars, sonar and labels), so the grey arrow when
  hiding is a game-side state that Online does not apply. Not fixable in a GFX.
- Base-game (2013) `.gfx` are not decompiled anywhere; only Enhanced code exists.

## Rules

- Do not guess a scaleform's behaviour from its filename; grep the scripts in `_scaleforms/`.
- `mod/` holds only shipped binaries; working art/JPEXS exports go in `src/<gfx>/art/`.
- Never commit extracted vanilla dumps, `_scaleforms/`, or `dist/`.
- When a change is made to a `.gfx`, record it in that file's `src/<gfx>/patch.json`.
