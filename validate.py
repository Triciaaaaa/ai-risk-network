#!/usr/bin/env python3
"""CI checks for the core graph and optional Atlas v2 data files."""
import json
import pathlib
import re
import sys

P = pathlib.Path(__file__).resolve().parent
DATA_DIR = P / "data"


def load(path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


nodes = load(DATA_DIR / "nodes.json")
edges = load(DATA_DIR / "edges.json")
errs = []
ids = set()
for node in nodes:
    for key in ("id", "name", "type", "cluster"):
        if not node.get(key):
            errs.append(f"node missing {key}: {node.get('id') or node}")
    if node.get("type") not in ("person", "org"):
        errs.append(f"bad type: {node.get('id')}")
    if node.get("id") in ids:
        errs.append(f"duplicate id: {node['id']}")
    ids.add(node.get("id"))
    if node.get("url") and not node["url"].startswith(("http://", "https://")):
        errs.append(f"non-web url on {node['id']}")
    blob = " ".join(str(node.get(key, "")) for key in ("affil", "focus", "writings"))
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+|\+\d{1,3}[ -]?\(?\d{2,4}\)?[ -]?\d{3,4}[ -]?\d{3,4}|\(?\d{3}\)?[ -]\d{3}-\d{4}", blob):
        errs.append(f"contact detail in text of {node['id']}")

for edge in edges:
    if edge.get("s") not in ids or edge.get("t") not in ids:
        errs.append(f"edge with unknown endpoint: {edge.get('s')} -> {edge.get('t')}")
    if not edge.get("label"):
        errs.append(f"edge without label: {edge.get('s')} -> {edge.get('t')}")
    if edge.get("u") and not edge["u"].startswith(("http://", "https://")):
        errs.append(f"edge source must be a web URL: {edge.get('s')} -> {edge.get('t')}")

topics_path = DATA_DIR / "topics.json"
if topics_path.exists():
    topics = load(topics_path)
    topic_ids = {
        item.get("id") if isinstance(item, dict) else item[0]
        for item in topics.get("taxonomy", [])
        if (isinstance(item, dict) and item.get("id")) or (isinstance(item, list) and item)
    }
    for node_id, values in topics.get("nodes", {}).items():
        if node_id not in ids:
            errs.append(f"topics.json has unknown node id: {node_id}")
        if not isinstance(values, dict):
            errs.append(f"topics.json values must be an object: {node_id}")
            continue
        for topic_id, probability in values.items():
            if topic_id not in topic_ids:
                errs.append(f"topics.json has unknown topic id: {node_id} -> {topic_id}")
            if not isinstance(probability, (int, float)) or not 0 <= probability <= 1:
                errs.append(f"topics.json has bad probability: {node_id} -> {topic_id} = {probability}")

history_path = DATA_DIR / "history.json"
if history_path.exists():
    history_data = load(history_path)
    for node_id, value in history_data.get("nodes", {}).items():
        if node_id not in ids:
            errs.append(f"history.json has unknown node id: {node_id}")
        if not isinstance(value, dict):
            errs.append(f"history.json values must be an object: {node_id}")

aliases_path = DATA_DIR / "aliases_zh.json"
if aliases_path.exists():
    aliases = load(aliases_path)
    if not isinstance(aliases, dict):
        errs.append("aliases_zh.json must be an object")
    else:
        for node_id, values in aliases.items():
            if node_id not in ids:
                errs.append(f"aliases_zh.json has unknown node id: {node_id}")
            if not isinstance(values, list) or not all(isinstance(value, str) and value.strip() for value in values):
                errs.append(f"aliases_zh.json aliases must be non-empty strings: {node_id}")

faq_path = DATA_DIR / "faq.json"
if faq_path.exists():
    faq = load(faq_path)
    if not isinstance(faq, list):
        errs.append("faq.json must be an array")
    else:
        faq_ids = set()
        valid_roles = {"research", "funding", "policy", "invest", "media", "curious"}
        for item in faq:
            if not isinstance(item, dict):
                errs.append("faq.json entries must be objects")
                continue
            faq_id = item.get("id")
            if not faq_id or faq_id in faq_ids:
                errs.append(f"faq.json has missing or duplicate id: {faq_id}")
            faq_ids.add(faq_id)
            if item.get("role") not in valid_roles:
                errs.append(f"faq.json has unknown role: {faq_id} -> {item.get('role')}")
            top10, why = item.get("top10"), item.get("why")
            if not isinstance(top10, list) or not isinstance(why, list):
                errs.append(f"faq.json top10 and why must be arrays: {faq_id}")
                continue
            if len(top10) != 10:
                errs.append(f"faq.json top10 must contain 10 node ids: {faq_id} ({len(top10)})")
            if len(top10) != len(why):
                errs.append(f"faq.json top10 and why length mismatch: {faq_id} ({len(top10)} != {len(why)})")
            if not all(isinstance(reason, str) and reason.strip() for reason in why):
                errs.append(f"faq.json why must contain non-empty strings: {faq_id}")
            for node_id in top10:
                if node_id not in ids:
                    errs.append(f"faq.json has unknown node id: {faq_id} -> {node_id}")

for error in errs[:50]:
    print("ERROR", error)
print(f"{len(nodes)} nodes, {len(edges)} edges, {len(errs)} errors")
sys.exit(1 if errs else 0)
