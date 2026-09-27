#!/usr/bin/env python3
"""Build the single-file site and deterministic structural communities."""
import collections
import json
import pathlib
import random

P = pathlib.Path(__file__).resolve().parent
DATA_DIR = P / "data"

RELATION_WEIGHTS = {
    "employed by": 1.0,
    "member of": 1.0,
    "board of": 1.0,
    "officer of": 1.0,
    "runs": 1.0,
    "founded": 1.0,
    "co-founded with": 1.0,
    "advises": 1.0,
    "mentor of": 1.0,
    "co-authored with": 0.7,
    "funds": 0.5,
    "grantee of": 0.5,
    "donated to": 0.5,
    "invested in": 0.5,
    "led round": 0.5,
    "co-invested": 0.5,
    "partners with": 1.0,
    "hosts": 1.0,
}


def load_json(path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def relation_type(edge):
    return str(edge.get("label", "")).split(" · ", 1)[0].strip().lower()


def structural_graph(edges):
    """Return a symmetric weighted adjacency map and the accepted source edges."""
    graph = collections.defaultdict(dict)
    accepted = []
    for edge in edges:
        kind = relation_type(edge)
        weight = RELATION_WEIGHTS.get(kind)
        source, target = edge.get("s"), edge.get("t")
        if weight is None or not source or not target or source == target:
            continue
        graph[source][target] = graph[source].get(target, 0.0) + weight
        graph[target][source] = graph[target].get(source, 0.0) + weight
        accepted.append((source, target, kind, weight))
    return {node: dict(neighbours) for node, neighbours in graph.items()}, accepted


def local_move(graph, seed):
    """One Louvain local-moving phase on a weighted undirected graph."""
    rng = random.Random(seed)
    nodes = sorted(graph, key=str)
    community = {node: index for index, node in enumerate(nodes)}
    degree = {node: sum(graph[node].values()) for node in nodes}
    total = {community[node]: degree[node] for node in nodes}
    m2 = sum(degree.values())
    if not m2:
        return community

    for _ in range(100):
        moved = False
        order = nodes[:]
        rng.shuffle(order)
        for node in order:
            old = community[node]
            k_i = degree[node]
            neighbour_weight = collections.defaultdict(float)
            for neighbour, weight in graph[node].items():
                if neighbour != node:
                    neighbour_weight[community[neighbour]] += weight
            total[old] -= k_i
            best, best_gain = old, 0.0
            for candidate in sorted(set(neighbour_weight) | {old}):
                gain = neighbour_weight.get(candidate, 0.0) - total.get(candidate, 0.0) * k_i / m2
                if gain > best_gain + 1e-12 or (abs(gain - best_gain) <= 1e-12 and candidate < best):
                    best, best_gain = candidate, gain
            community[node] = best
            total[best] = total.get(best, 0.0) + k_i
            if best != old:
                moved = True
        if not moved:
            break

    groups = collections.defaultdict(list)
    for node, group in community.items():
        groups[group].append(node)
    order = sorted(groups, key=lambda group: tuple(sorted(map(str, groups[group]))))
    renumber = {group: index for index, group in enumerate(order)}
    return {node: renumber[group] for node, group in community.items()}


def aggregate_graph(graph, partition):
    """Collapse communities; diagonal weights store twice the internal edge weight."""
    result = collections.defaultdict(dict)
    nodes = sorted(graph, key=str)
    for source in nodes:
        source_group = partition[source]
        for target, weight in graph[source].items():
            if source == target:
                result[source_group][source_group] = result[source_group].get(source_group, 0.0) + weight
            elif str(source) < str(target):
                target_group = partition[target]
                if source_group == target_group:
                    result[source_group][source_group] = result[source_group].get(source_group, 0.0) + 2.0 * weight
                else:
                    result[source_group][target_group] = result[source_group].get(target_group, 0.0) + weight
                    result[target_group][source_group] = result[target_group].get(source_group, 0.0) + weight
    for group in set(partition.values()):
        result.setdefault(group, {})
    return {node: dict(neighbours) for node, neighbours in result.items()}


def modularity(partition, accepted):
    total_weight = sum(weight for _, _, _, weight in accepted)
    if not total_weight:
        return 0.0
    degree = collections.defaultdict(float)
    inside = collections.defaultdict(float)
    for source, target, _, weight in accepted:
        degree[partition[source]] += weight
        degree[partition[target]] += weight
        if partition[source] == partition[target]:
            inside[partition[source]] += weight
    return sum(inside[group] / total_weight - (value / (2.0 * total_weight)) ** 2 for group, value in degree.items())


def louvain(graph, accepted, seed):
    """Run Louvain levels and return an original-node partition plus modularity."""
    current_graph = graph
    members = {node: {node} for node in graph}
    best_partition = {node: index for index, node in enumerate(sorted(graph))}
    best_modularity = modularity(best_partition, accepted)

    for level in range(100):
        level_partition = local_move(current_graph, seed * 1009 + level)
        next_members = collections.defaultdict(set)
        for node, group in level_partition.items():
            next_members[group].update(members[node])
        original_partition = {}
        ordered_groups = sorted(next_members, key=lambda group: tuple(sorted(next_members[group])))
        for index, group in enumerate(ordered_groups):
            for node in next_members[group]:
                original_partition[node] = index
        score = modularity(original_partition, accepted)
        if score > best_modularity + 1e-12:
            best_partition, best_modularity = original_partition, score
        if len(next_members) == len(current_graph):
            break
        current_graph = aggregate_graph(current_graph, level_partition)
        members = {group: originals for group, originals in next_members.items()}

    return best_partition, best_modularity


def taxonomy_map(topics):
    result = {}
    for item in (topics or {}).get("taxonomy", []):
        if isinstance(item, dict) and item.get("id"):
            result[item["id"]] = {"id": item["id"], "zh": item.get("zh", item["id"]), "en": item.get("en", "")}
        elif isinstance(item, list) and item:
            result[item[0]] = {"id": item[0], "zh": item[1] if len(item) > 1 else item[0], "en": item[2] if len(item) > 2 else ""}
    return result


def topic_enrichment(members, graph_nodes, topics):
    if not topics or not topics.get("nodes"):
        return []
    taxonomy = taxonomy_map(topics)
    scores = topics["nodes"]
    global_mean = {}
    for topic_id in taxonomy:
        global_mean[topic_id] = sum(float(scores.get(node, {}).get(topic_id, 0.0)) for node in graph_nodes) / len(graph_nodes)
    enriched = []
    for topic_id, label in taxonomy.items():
        mean = sum(float(scores.get(node, {}).get(topic_id, 0.0)) for node in members) / len(members)
        if mean <= 0.0 or global_mean[topic_id] <= 0.0:
            continue
        enriched.append({**label, "mean": round(mean, 3), "lift": round(mean / global_mean[topic_id], 2)})
    enriched.sort(key=lambda item: (-item["lift"], -item["mean"], item["id"]))
    return enriched[:3]


def community_payload(nodes, edges, topics=None):
    graph, accepted = structural_graph(edges)
    if not graph:
        return {"method": "louvain", "runs": 10, "modularity": 0.0, "selected_seed": 0, "nodes": {}, "list": []}

    runs = []
    for seed in range(10):
        partition, score = louvain(graph, accepted, seed)
        runs.append((score, seed, partition))
    best_score, best_seed, best = max(runs, key=lambda item: (item[0], -item[1]))
    raw_groups = collections.defaultdict(list)
    for node, group in best.items():
        raw_groups[group].append(node)
    ordered = sorted(raw_groups.values(), key=lambda members: (-len(members), tuple(sorted(members))))
    id_for_group = {best[members[0]]: f"C{index:02d}" for index, members in enumerate(ordered, 1)}
    node_to_community = {node: id_for_group[group] for node, group in best.items()}
    node_data = {node["id"]: node for node in nodes}
    weighted_degree = {node: sum(neighbours.values()) for node, neighbours in graph.items()}
    graph_nodes = sorted(graph)

    coassigned = {}
    for members in ordered:
        if len(members) < 2:
            coassigned[best[members[0]]] = 1.0
            continue
        together, pairs = 0, 0
        for index, source in enumerate(members):
            for target in members[index + 1:]:
                together += sum(1 for _, _, partition in runs if partition[source] == partition[target])
                pairs += len(runs)
        coassigned[best[members[0]]] = together / pairs

    relation_counts = collections.defaultdict(collections.Counter)
    for source, target, kind, _ in accepted:
        if best[source] == best[target]:
            relation_counts[best[source]][kind] += 1

    summaries = []
    for members in ordered:
        members = sorted(members)
        group = best[members[0]]
        top_nodes = sorted(members, key=lambda node: (-weighted_degree.get(node, 0.0), node))[:5]
        clusters = collections.Counter(
            node_data[node].get("cluster", "other")
            for node in members
            if node_data.get(node, {}).get("type") == "person"
        )
        summaries.append({
            "id": id_for_group[group],
            "size": len(members),
            "stability": round(coassigned[group], 3),
            "members": members,
            "top_nodes": [{"id": node, "degree": round(weighted_degree.get(node, 0.0), 1)} for node in top_nodes],
            "clusters": [{"id": key, "count": value} for key, value in sorted(clusters.items(), key=lambda item: (-item[1], item[0]))],
            "relations": [{"type": key, "count": value} for key, value in relation_counts[group].most_common(5)],
            "topics": topic_enrichment(members, graph_nodes, topics),
        })

    return {
        "method": "louvain",
        "runs": 10,
        "modularity": round(best_score, 6),
        "selected_seed": best_seed,
        "eligible_relations": len(accepted),
        "nodes": node_to_community,
        "list": summaries,
    }


def main():
    nodes = load_json(DATA_DIR / "nodes.json")
    edges = load_json(DATA_DIR / "edges.json")
    data = {"nodes": nodes, "edges": edges}
    ids = {node["id"] for node in nodes}
    bad = [edge for edge in edges if edge["s"] not in ids or edge["t"] not in ids]
    if bad:
        raise SystemExit(f"{len(bad)} edges reference unknown node ids, e.g. {bad[0]}")

    for key, filename in (("topics", "topics.json"), ("history", "history.json"), ("aliases", "aliases_zh.json")):
        path = DATA_DIR / filename
        if path.exists():
            data[key] = load_json(path)
    data["communities"] = community_payload(nodes, edges, data.get("topics"))

    template = (P / "template.html").read_text(encoding="utf-8")
    if template.count("/*DATA*/") != 1:
        raise SystemExit("template.html must contain exactly one /*DATA*/ placeholder")
    (P / "index.html").write_text(
        template.replace("/*DATA*/", json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)),
        encoding="utf-8",
    )
    communities = data["communities"]
    print(
        "index.html rebuilt:", len(nodes), "nodes,", len(edges), "edges,",
        len(communities["list"]), "communities, modularity", f'{communities["modularity"]:.6f}',
    )


if __name__ == "__main__":
    main()
