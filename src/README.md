# src/

One directory per modded `.gfx`, named after the scaleform. Each holds:

- `patch.json` — what the vanilla file was, and every change made to it.
- `art/` — the loose source assets used (`.dds`, `.png`, `.psd`), if any.

`patch.json` is the file you reopen when the game updates. It is deliberately
plain JSON so it diffs readably in git.

## Schema

```json
{
  "target": "update/update.rpf/x64/data/cdimages/scaleform_frontend.rpf/loadingscreen_startup.gfx",
  "vanilla_build": "1.0.3411",
  "base_sha256": "<sha256 of the vanilla gfx this was built from>",
  "summary": "one line describing the intent",
  "changes": []
}
```

`target` must match the path used in the vanilla manifest (relative to the
manifest root). `base_sha256` is copied from `vanilla/<build>.json`; it is how
`tools/compare.py --src` knows a patch is stale.

## Change entries

Use whatever is precise enough to replay the edit by hand:

| `kind` | Fields worth recording |
| --- | --- |
| `image` | `image_id`, `export_name`, `file_name`, `target_width`, `target_height`, `bitmap_format`, `art`, `dependent_characters` |
| `bitmap-fill` | `shape` or `sprite`, `from_image`, `to_image` |
| `tag` | `tag`, `character_id`, `set` (field values), `position` (where in the tag list) |
| `script` | `class`, `method`, `note` — and the edited `.as` file next to the patch |
| `note` | `text` — for anything that cannot be expressed as a field change |

Record character IDs and image names, not "the ring sprite" — names drift, IDs
are what you need when the file is reopened.

## Example

See [`loadingscreen_startup/patch.json`](loadingscreen_startup/patch.json).
