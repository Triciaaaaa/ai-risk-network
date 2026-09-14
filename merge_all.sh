#!/bin/bash
# Owner-run: merge the open agent PRs one by one, rebuilding each on the latest main first.
#   bash ~/research/ai-risk-network/merge_all.sh            # cleanup PR first, then the rest in ascending order
#   bash ~/research/ai-risk-network/merge_all.sh 8 9        # or an explicit order
set -uo pipefail
REPO=Triciaaaaa/ai-risk-network
export PATH="$PATH:/usr/local/bin:/opt/homebrew/bin"
if [ $# -gt 0 ]; then PRS="$*"; else
  ALL=$(gh pr list -R $REPO --json number,headRefName --jq '.[] | "\(.number) \(.headRefName)"')
  FIRST=$(echo "$ALL" | awk '$2 ~ /^cleanup\// {print $1}')
  REST=$(echo "$ALL" | awk '$2 !~ /^cleanup\// {print $1}' | sort -n | tr '\n' ' ')
  PRS="$FIRST $REST"
fi
echo "order: $PRS"
for n in $PRS; do
  echo "== PR #$n"
  /usr/bin/python3 ~/research/xrisk-atlas/agent/issue_agent.py 2>&1 | grep -i "refresh" || true
  m=""
  for i in $(seq 1 12); do
    m=$(gh pr view $n -R $REPO --json mergeable --jq .mergeable 2>/dev/null); [ "$m" = "MERGEABLE" ] && break; sleep 8
  done
  if [ "$m" = "MERGEABLE" ]; then gh pr merge $n -R $REPO --squash --delete-branch && echo "merged #$n"; else echo "skip #$n (mergeable=$m)"; fi
done
cd ~/research/ai-risk-network && git checkout -q main && git pull -q --ff-only origin main
python3 -c "import json;N=json.load(open('data/nodes.json'));E=json.load(open('data/edges.json'));print('main now:',len(N),'nodes,',sum(1 for n in N if n['type']=='person'),'people,',len(E),'edges')"
echo "open PRs left: $(gh pr list -R $REPO --json number --jq 'length')"
