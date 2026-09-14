#!/usr/bin/env python3
"""CI check for pull requests: schema, unique ids, sourced edges, no contact details in text."""
import json, re, sys, pathlib
P = pathlib.Path(__file__).resolve().parent
nodes = json.load(open(P/'data/nodes.json')); edges = json.load(open(P/'data/edges.json'))
errs = []; ids = set()
for n in nodes:
    for k in ('id', 'name', 'type', 'cluster'):
        if not n.get(k): errs.append(f"node missing {k}: {n.get('id') or n}")
    if n.get('type') not in ('person', 'org'): errs.append(f"bad type: {n.get('id')}")
    if n.get('id') in ids: errs.append(f"duplicate id: {n['id']}")
    ids.add(n.get('id'))
    if n.get('url') and not n['url'].startswith(('http://', 'https://')): errs.append(f"non-web url on {n['id']}")
    blob = ' '.join(str(n.get(k, '')) for k in ('affil', 'focus', 'writings'))
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+|\+\d{1,3}[ -]?\(?\d{2,4}\)?[ -]?\d{3,4}[ -]?\d{3,4}|\(?\d{3}\)?[ -]\d{3}-\d{4}", blob): errs.append(f"contact detail in text of {n['id']}")
for e in edges:
    if e.get('s') not in ids or e.get('t') not in ids: errs.append(f"edge with unknown endpoint: {e.get('s')} -> {e.get('t')}")
    if not e.get('label'): errs.append(f"edge without label: {e.get('s')} -> {e.get('t')}")
    if e.get('u') and not e['u'].startswith(('http://', 'https://')): errs.append(f"edge source must be a web URL: {e.get('s')} -> {e.get('t')}")
for x in errs[:50]: print('ERROR', x)
print(f"{len(nodes)} nodes, {len(edges)} edges, {len(errs)} errors")
sys.exit(1 if errs else 0)
