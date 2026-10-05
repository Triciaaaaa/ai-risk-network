#!/usr/bin/env python3
"""Generate data/aliases_zh.json from the reviewed bilingual seed list."""
import collections
import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parents[1]


def base_name(value):
    return re.sub(r"\s*[\uff08(][^\uff09)]*[\uff09)]\s*", " ", value).strip()


nodes = json.loads((P / "data/nodes.json").read_text(encoding="utf-8"))
exact = collections.defaultdict(list)
base = collections.defaultdict(list)
for node in nodes:
    exact[node["name"]].append(node["id"])
    base[base_name(node["name"])].append(node["id"])

result = collections.defaultdict(list)
matched_rows = discarded_rows = 0
for raw in (P / "tools/aliases_zh_seed.txt").read_text(encoding="utf-8").splitlines():
    if not raw.strip() or raw.lstrip().startswith("#"):
        continue
    try:
        english, chinese = raw.split("\t", 1)
    except ValueError:
        discarded_rows += 1
        continue
    candidates = exact.get(english, []) or base.get(english, [])
    if len(candidates) != 1:
        discarded_rows += 1
        continue
    matched_rows += 1
    for alias in chinese.split("|"):
        alias = alias.strip()
        if alias and alias not in result[candidates[0]]:
            result[candidates[0]].append(alias)

output = {node_id: result[node_id] for node_id in sorted(result)}
(P / "data/aliases_zh.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(
    "aliases_zh.json generated:", matched_rows, "matched seed rows,",
    discarded_rows, "discarded,", len(output), "nodes,",
    sum(map(len, output.values())), "aliases",
)
