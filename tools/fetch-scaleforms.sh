#!/usr/bin/env bash
# Fetch the decompiled GTA V Enhanced scaleform scripts used for reference.
#
# Clones eternights/decompiled-scaleforms-gtav as a blobless, sparse checkout
# limited to **/scripts/** (about 52 MB). No game files or credentials needed.
#
# Usage:
#   bash tools/fetch-scaleforms.sh [repo-url] [destination]
#
# Defaults: the public GitHub repo and ./_scaleforms (gitignored).

set -euo pipefail

REPO="${1:-https://github.com/eternights/decompiled-scaleforms-gtav.git}"
DEST="${2:-_scaleforms}"

if [ -e "$DEST" ]; then
    echo "error: $DEST already exists" >&2
    echo "       remove it first, or pass a different destination:" >&2
    echo "       bash tools/fetch-scaleforms.sh '$REPO' other_dir" >&2
    exit 1
fi

git clone --filter=blob:none --no-checkout --depth 1 "$REPO" "$DEST"
git -C "$DEST" sparse-checkout set --no-cone '**/scripts/**'
git -C "$DEST" checkout

count=$(find "$DEST" -name '*.as' | wc -l | tr -d ' ')
echo "fetched $count .as files into $DEST"
