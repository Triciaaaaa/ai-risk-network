#!/bin/bash
# Owner-run: copy the latest map + data from xrisk-atlas, validate, build, and push to a PUBLIC GitHub repo
# with GitHub Pages enabled. Re-run any time to publish an update.
#   bash ~/research/ai-risk-network/publish_github.sh
set -euo pipefail
cd "$(dirname "$0")"
REPO=ai-risk-network
SRC=~/research/xrisk-atlas
mkdir -p data
cp "$SRC/site/template.html" template.html
cp "$SRC/data/network/nodes.json" "$SRC/data/network/edges.json" data/
python3 "$SRC/scripts/scan_sensitive_site.py" >/dev/null || { echo "sensitivity scan failed on site_dist; fix before publishing"; exit 1; }
python3 validate.py
python3 build.py
printf '.DS_Store\n__pycache__/\n' > .gitignore
[ -d .git ] || git init -q -b main
git add -A
git diff --cached --quiet || git commit -qm "update map and data ($(date +%F))"
if ! gh repo view "$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" --public --source . --push --description "AI risk fund & member network: who funds, runs and co-authors with whom, every edge sourced"
  gh api -X POST "repos/{owner}/$REPO/pages" -f 'source[branch]=main' -f 'source[path]=/' >/dev/null || true
else
  git push -u origin main
fi
OWNER=$(gh api user --jq .login)
echo "repo:  https://github.com/$OWNER/$REPO"
echo "pages: https://$OWNER.github.io/$REPO/   (first deploy takes ~1 min; Settings → Pages shows status)"
