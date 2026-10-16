#!/usr/bin/env bash
# Build BioStack and publish dist/ to the gh-pages branch (GitHub Pages, legacy branch source).
# Usage: scripts/deploy-pages.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH=/home/box/.local/node22/bin:$PATH
SITE_URL=https://yonghaozhao722.github.io BASE_PATH=/biostack npm run build
touch dist/.nojekyll
REMOTE=$(git remote get-url origin)
TMP=$(mktemp -d)
cp -r dist/. "$TMP"
cd "$TMP"
git init -q -b gh-pages
git add -A
git commit -qm "Deploy $(date -u +%Y-%m-%dT%H:%MZ)"
git push -f "$REMOTE" gh-pages
rm -rf "$TMP"
echo "Pushed. Live at https://yonghaozhao722.github.io/biostack/ in ~1 min."
