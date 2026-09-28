# 贡献指南 / Contributing Guide

[中文](#中文) · [English](#english)

## 中文

小改动也有用。补一个别名、一个年份来源或一段简介，通常十分钟内可以完成。

### 三种贡献方式

1. **提 issue：**使用[添加条目](https://github.com/Triciaaaaa/ai-risk-network/issues/new?template=add-request.yml)、[修正数据](https://github.com/Triciaaaaa/ai-risk-network/issues/new?template=fix-request.yml)或[删除请求](https://github.com/Triciaaaaa/ai-risk-network/issues/new?template=remove-request.yml)表单。不熟悉 JSON 时，选这种方式。
2. **改 JSON 后提 pull request：**编辑 `data/nodes.json`、`data/edges.json` 或相应扩展文件。一个 PR 只处理一组相关改动。
3. **补中文别名：**在 `data/aliases_zh.json` 中给已有节点添加常用中文名。别名必须能从公开页面核对，不能加入联系方式、私下称呼或推测身份。

提交前请先读 [`docs/INCLUSION.md`](docs/INCLUSION.md)。

### JSON 字段规范

#### `data/nodes.json`

每个节点至少包含：

- `id`：稳定、唯一的 kebab-case 标识符。已有节点不要随意改 `id`。
- `name`：公开使用的名称。
- `type`：只能是 `person` 或 `org`。
- `cluster`：沿用现有展示类别。不要用它表达赞成、反对或信誉判断。

可选字段：

- `affil`：公开角色或机构关联的简短事实。
- `focus`：公开研究或工作主题。
- `writings`：公开写作或研究成果的简短说明。
- `url`：以 `http://` 或 `https://` 开头的公开页面。
- `deg`、`x`、`y`：地图的关系数和布局字段。普通资料修正不要改这些字段。

新增节点必须与现有图至少有一条符合收录标准的关系。不要只加孤立节点。

#### `data/edges.json`

- `s`、`t`：必须引用 `nodes.json` 中已有的节点 `id`。
- `label`：使用 `关系类型 · 简短事实` 格式，例如 `funds · 2025`。只写来源能支持的事实。
- `arrow`：从 `s` 指向 `t` 时写 `1->2`；无方向时写空字符串。
- `dash`：公开结盟、公开反对等较软关系写 `true`；其余通常写 `false`。
- `scale`：通常沿用相近关系的显示权重。
- `u`：直接支持该关系的公开网页 URL。

**一条关系至少给一个公开来源。** 如果多个来源分别支持不同事实，请拆成清楚的关系，或在说明中列出每个来源。优先使用机构公告、论文、作者页、资助记录、公开声明或论坛原文。搜索结果页、无来源转载和私人材料不够。

#### 扩展文件

- `data/topics.json`：`taxonomy` 定义主题；`nodes` 把节点 `id` 映射到 0 到 1 的主题权重。不要手工猜权重。
- `data/history.json`：记录机构沿革及其来源。保留 `source`、`fetched`、`match_rule`、`qid` 和验证字段；不要把不确定的同名机构合并。
- `data/aliases_zh.json`：对象键是节点 `id`，值是非空字符串数组。使用常见简体中文名，避免重复和自造译名。

JSON 使用 UTF-8、双引号和合法 JSON 语法。尽量只改需要的对象，不要重排或格式化整个大文件。

### 本地检查

在仓库根目录运行：

```bash
python3 validate.py
python3 build.py
```

`validate.py` 检查必填字段、节点引用、URL、扩展文件和明显的联系方式。`build.py` 验证数据能生成页面，并会重写 `index.html`。检查完成后，不要把生成的 `index.html` 放进数据 PR；合并到 `main` 后，CI 会重建它。

### Pull request 规范

- 一个 PR 只做一件事，标题直接说明添加或修正了什么。
- 在 PR 描述中列出来源，并说明每个来源支持哪条事实。
- 数据 PR 只包含相关的 `data/*.json` 改动。不要夹带 `index.html`、工具、样式、批量格式化或其他无关文件。
- 不提交联系方式、私人材料、家庭关系或“谁认识谁”的推测。
- 提交前运行 `python3 validate.py` 和 `python3 build.py`，并写明结果。
- 修正现有关系时，保留可核查的事实；若来源失效，请给替代公开来源或解释删除理由。

### 适合新人的任务

- 给已有节点补一个可核查的中文别名。
- 给机构补成立年份及公开来源。
- 把一段现有简介翻译成简短中文或英文。
- 修复失效的来源链接，但不改变原事实。
- 找出重复别名或明显的拼写错误。

---

## English

Small changes are useful. A Chinese alias, a sourced founding year, or a short translated description can usually be contributed in ten minutes.

### Three ways to contribute

1. **File an issue.** Use the [add](https://github.com/Triciaaaaa/ai-risk-network/issues/new?template=add-request.yml), [correction](https://github.com/Triciaaaaa/ai-risk-network/issues/new?template=fix-request.yml), or [removal](https://github.com/Triciaaaaa/ai-risk-network/issues/new?template=remove-request.yml) form if you do not want to edit JSON.
2. **Edit JSON and open a pull request.** Change `data/nodes.json`, `data/edges.json`, or the relevant extension file. Keep each pull request to one related set of changes.
3. **Add Chinese aliases.** Add a common Chinese name for an existing node in `data/aliases_zh.json`. The alias must be checkable on a public page. Do not add contact details, private nicknames, or inferred identities.

Read [`docs/INCLUSION.md`](docs/INCLUSION.md) before submitting data.

### JSON field rules

#### `data/nodes.json`

Every node needs:

- `id`: a stable, unique kebab-case identifier. Do not casually rename existing IDs.
- `name`: the publicly used name.
- `type`: either `person` or `org`.
- `cluster`: an existing display category, never a statement of approval, opposition, or reputation.

Optional fields are `affil` for short public role facts, `focus` for public topics, `writings` for short notes on public work, and `url` for a public `http://` or `https://` page. `deg`, `x`, and `y` are map count and layout fields; ordinary factual corrections should not change them.

A new node must have at least one in-scope relation to the existing graph. Do not add isolated nodes.

#### `data/edges.json`

- `s` and `t` must refer to existing node IDs.
- `label` uses `relation type · short fact`, such as `funds · 2025`. Include only what the source supports.
- `arrow` is `1->2` when the relation runs from `s` to `t`, or an empty string when it is undirected.
- `dash` is `true` for softer public relations such as explicit alliance or opposition; it is usually `false` otherwise.
- `scale` normally follows comparable existing relations.
- `u` is the public webpage that directly supports the relation.

**Give every relation at least one public source.** If different sources support different facts, split the facts into clear relations or identify each source in the pull-request description. Prefer organisation announcements, papers, author pages, grant records, public statements, and original forum posts. Search result pages, unsourced reposts, and private material are insufficient.

#### Extension files

- `data/topics.json`: `taxonomy` defines topics; `nodes` maps node IDs to topic weights from 0 to 1. Do not guess weights by hand.
- `data/history.json`: stores organisation history and provenance. Preserve `source`, `fetched`, `match_rule`, `qid`, and verification fields. Do not merge uncertain namesakes.
- `data/aliases_zh.json`: keys are node IDs and values are arrays of non-empty strings. Use established Simplified Chinese names and avoid duplicates or invented translations.

Use UTF-8, double quotes, and valid JSON. Change only the needed objects; do not reformat or reorder a whole large file.

### Local checks

Run from the repository root:

```bash
python3 validate.py
python3 build.py
```

`validate.py` checks required fields, node references, URLs, extension files, and obvious contact details. `build.py` confirms that the data can produce the site and rewrites `index.html`. After the check, keep generated `index.html` out of data pull requests; CI rebuilds it after merge to `main`.

### Pull-request rules

- Keep one pull request to one purpose, with a title that states the change.
- List sources in the description and say which fact each source supports.
- A data pull request should contain only the relevant `data/*.json` changes. Exclude `index.html`, tools, styling, bulk formatting, and unrelated files.
- Do not submit contact details, private material, family relations, or guesses about “who knows whom.”
- Run `python3 validate.py` and `python3 build.py` and report the results.
- When correcting a relation, preserve facts that remain verifiable. If a source is dead, provide a replacement public source or explain why the relation should be removed.

### Good first issues

- Add a verifiable Chinese alias to an existing node.
- Add a sourced founding year to an organisation.
- Translate an existing short description into concise Chinese or English.
- Replace a dead source link without changing the underlying fact.
- Find duplicate aliases or clear spelling errors.
