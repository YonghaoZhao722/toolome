#!/usr/bin/env bash
# Build Toolome and publish dist/ to the gh-pages branch (GitHub Pages, legacy branch source).
# Usage: scripts/deploy-pages.sh
# Config (site.config.json, or env overrides):
#   customDomain / CUSTOM_DOMAIN                 e.g. toolome.org -> writes dist/CNAME, builds at site root
#   googleSiteVerification / GOOGLE_SITE_VERIFICATION -> <meta name="google-site-verification">
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH=/home/box/.local/node22/bin:$PATH
DOMAIN=${CUSTOM_DOMAIN:-$(python3 -c "import json;print(json.load(open('site.config.json')).get('customDomain',''))")}
if [ -n "$DOMAIN" ]; then
  SITE_URL=https://$DOMAIN BASE_PATH=/ npm run build
  echo "$DOMAIN" > dist/CNAME
  LIVE=https://$DOMAIN/
else
  SITE_URL=https://yonghaozhao722.github.io BASE_PATH=/toolome npm run build
  LIVE=https://yonghaozhao722.github.io/toolome/
fi
touch dist/.nojekyll
REMOTE=$(git remote get-url origin)
NAME=$(git config user.name); EMAIL=$(git config user.email)
TMP=$(mktemp -d)
cp -r dist/. "$TMP"
cd "$TMP"
git init -q -b gh-pages
git add -A
git -c user.name="$NAME" -c user.email="$EMAIL" commit -qm "Deploy $(date -u +%Y-%m-%dT%H:%MZ)"
git push -f "$REMOTE" gh-pages
rm -rf "$TMP"
echo "Pushed. Live at $LIVE in ~1 min."
