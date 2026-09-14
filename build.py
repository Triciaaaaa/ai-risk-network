#!/usr/bin/env python3
"""Rebuild index.html from template.html + data/nodes.json + data/edges.json (no dependencies)."""
import json, pathlib
P = pathlib.Path(__file__).resolve().parent
data = {"nodes": json.load(open(P/'data/nodes.json')), "edges": json.load(open(P/'data/edges.json'))}
ids = {n['id'] for n in data['nodes']}
bad = [e for e in data['edges'] if e['s'] not in ids or e['t'] not in ids]
if bad:
    raise SystemExit(f"{len(bad)} edges reference unknown node ids, e.g. {bad[0]}")
(P/'index.html').write_text((P/'template.html').read_text().replace('/*DATA*/', json.dumps(data, ensure_ascii=False)))
print('index.html rebuilt:', len(data['nodes']), 'nodes,', len(data['edges']), 'edges')
