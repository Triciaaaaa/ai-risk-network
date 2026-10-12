# AI Risk Network

[中文](#中文) · [English](#english) · [在线地图 / Live map](https://triciaaaaa.github.io/ai-risk-network/)

## 中文

AI Risk Network 是一张可下载、可核查来源的公开关系图，用来查看 AI 风险领域中的人物、机构、资金、任职、合著和公开立场。

### 为什么做

中文世界缺少一份带来源、可共同维护的 AI 风险生态图。公开信息散落在机构网站、资助公告、论文和论坛页面里。这个项目把它们整理成结构化数据，并保留每条关系的公开来源，方便读者回到原文核查。

### 能做什么

- **浏览地图：**圆形是人物，方形是机构。颜色表示研究、AI 安全机构、资助、实验室、政策、媒体等类型。橙线表示资金，灰线表示任职或创办等关系，蓝线表示合著或公开结盟，青线表示论坛活动。总览默认绘制至少有 4 条关系的节点；放大后可看长尾。
- **搜索和问答：**搜索名字，或直接输入“谁在资助 interpretability”“某机构的董事会”等中英文问题。页面会列出匹配关系及来源，并在图上高亮。点击名字可打开节点详情，也可从详情返回问题结果。
- **“我该关注谁”：**写下工作或兴趣，再选择研究、找资助、政策、投资或写作等身份。页面按公开数据的相关度排列人物、机构和关系。结果是相关度排序，不是引荐名单。
- **查看机构沿革：**机构页会汇总成立、前身、后继、母机构、创办、任职和资金事件。部分基础资料来自 Wikidata。
- **查看结构社区实验：**页面按公开关系做结构聚类，只显示 `C01`、`C02` 这类中性编号。它是探索性结果，不是阵营判断。
- **分享当前视图：**节点、问题，或推荐输入及所选身份会写入链接，复制网址即可分享当前页面。

问答和“我该关注谁”都在浏览器内运行。输入不会发送到服务器，也不会被保存。项目不计算人与人之间的路径，不提供“谁认识谁”或引荐链。

### 数据规模与模型

当前快照（2026-09-28）包含 **1,790 个节点**（1,173 人、617 个机构）和 **6,221 条关系**。

`data/nodes.json` 是节点数组：

| 字段 | 含义 |
|---|---|
| `id` | 稳定的 kebab-case 标识符 |
| `name` | 公开名称 |
| `type` | `person` 或 `org` |
| `cluster` | 展示用类别 |
| `affil`, `focus`, `writings` | 可选的公开简介、研究方向和写作信息 |
| `url` | 可选的公开页面 |
| `deg`, `x`, `y` | 地图使用的关系数和布局字段 |

`data/edges.json` 是关系数组：

| 字段 | 含义 |
|---|---|
| `s`, `t` | 起点和终点的节点 `id` |
| `label` | 关系类型及简短事实，例如 `funds · 2025` |
| `arrow` | `1->2` 表示有向关系；空字符串表示无向关系 |
| `dash` | 是否用虚线显示较软的公开关系 |
| `scale` | 显示权重 |
| `u` | 支持这条关系的公开来源 URL |

Atlas v2 还读取三个扩展文件：

- [`data/topics.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/topics.json)：主题分类表、标注模型和每个节点的主题权重。
- [`data/history.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/history.json)：机构沿革、匹配规则和 Wikidata 条目；这部分源数据按 CC0 使用。
- [`data/aliases_zh.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/aliases_zh.json)：节点 `id` 到中文别名数组的映射，用于中文搜索。

### 论坛数据口径

LessWrong 和 Alignment Forum 数据来自论坛公开 API，也就是公开个人页和帖子页展示的数据。

- 图中已有的人物只要在论坛发过内容，就会获得一条 `writes on` 关系，附帖子数、评论数、karma 快照和个人页来源。
- 缺失的高活跃作者按固定门槛加入：Alignment Forum 常驻作者需 AF karma 300+ 且有 5+ 篇 AF 帖子；AI 主题作者需有至少 3 篇 karma 100+ 的 AI 帖子；LessWrong 头部作者需总 karma 8,000+、至少 5 篇 karma 100+ 帖子，其中至少 5 篇属于 AI 主题。低活跃账号不收。
- 一篇论坛文章最多 6 位作者时，图中共同作者之间可加入 `co-authored with` 关系，并链接到原文。
- 只有账号自己公开表明身份时，才把账号与实名人物对应。笔名作者保留公开使用的笔名。计数是导入日期的公开快照。

### 原则

- 只收公开信息，不收联系方式、私人材料或家庭关系。
- 一条关系对应至少一个公开来源。读者应能打开来源核查。
- 不计算人与人之间的路径，不回答“谁认识谁”。
- 访客输入留在浏览器，不接后端模型，不发送到服务器。
- 收录、分类和结构社区编号都不代表支持、反对、信誉评价或重要性判断。
- 当事人或代理提出删除时，无条件处理。完整规则见[收录标准](docs/INCLUSION.md)。

### 如何贡献

可以提交添加、修正或删除请求，也可以直接修改 JSON 后提 pull request。最快的入门任务是补中文别名、给机构沿革补公开来源，或翻译一段公开简介。操作步骤和字段规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

### 数据下载

- [`nodes.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/nodes.json)：人物和机构节点。
- [`edges.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/edges.json)：带方向、标签和来源的关系。
- [`topics.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/topics.json)：节点主题权重。
- [`history.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/history.json)：机构沿革和 Wikidata 来源信息。
- [`aliases_zh.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/aliases_zh.json)：中文别名。

### 如何引用

引用信息见 [`CITATION.cff`](CITATION.cff)。GitHub 仓库页也会显示 “Cite this repository”。

### 许可

代码采用 [MIT License](LICENSE)。`data/` 下的数据采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，复用时请署名。`history.json` 中标明来自 Wikidata 的部分沿用 [CC0](https://creativecommons.org/publicdomain/zero/1.0/)。

---

## English

AI Risk Network is a downloadable, source-backed public graph of people, organisations, funding, roles, co-authorship, and public positions in the AI-risk field.

### Why this exists

Public information about this field is scattered across organisation websites, grant announcements, papers, and forums. The project turns those records into structured data and keeps a public source with each relation so readers can check the original material.

### What it can do

- **Explore the map.** Circles are people and squares are organisations. Colours represent research, AI-safety organisations, funders, labs, policy, media, and other groups. Orange lines show money, grey lines show roles and founding, blue lines show co-authorship and public alliances, and teal lines show forum activity. The overview draws nodes with at least four relations; zooming reveals the long tail.
- **Search and ask questions.** Search for a name or enter an English or Chinese question such as “who funds interpretability” or “the board of an organisation.” The page lists matching relations with sources and highlights them on the map. Node panels link back to the question results.
- **Use “Who should I follow?”** Describe your work or interests and choose a role such as research, seeking funding, policy, investing, or writing. The page ranks relevant people, organisations, and relations from the published data. It is a relevance ranking, not an introduction list.
- **Read organisation histories.** Organisation pages combine founding, predecessor, successor, parent, role, and funding events. Some basic facts come from Wikidata.
- **Inspect the structural-community experiment.** Public relations are clustered under neutral identifiers such as `C01` and `C02`. These exploratory groups are not ideological labels.
- **Share a view.** A node, a question, or recommendation input and its selected role are encoded in the URL, so copying the address preserves the current view.

Questions and “Who should I follow?” run entirely in the browser. Input is neither sent to a server nor stored. The project does not calculate paths between people and does not provide “who knows whom” or introduction chains.

### Dataset size and model

The current snapshot (2026-09-28) contains **1,790 nodes** (1,173 people and 617 organisations) and **6,221 relations**.

`data/nodes.json` is an array of nodes:

| Field | Meaning |
|---|---|
| `id` | Stable kebab-case identifier |
| `name` | Public name |
| `type` | `person` or `org` |
| `cluster` | Display category |
| `affil`, `focus`, `writings` | Optional public descriptions, topics, and writing notes |
| `url` | Optional public page |
| `deg`, `x`, `y` | Relation count and map-layout fields |

`data/edges.json` is an array of relations:

| Field | Meaning |
|---|---|
| `s`, `t` | Source and target node `id` values |
| `label` | Relation type and short factual detail, for example `funds · 2025` |
| `arrow` | `1->2` for a directed relation; an empty string for an undirected relation |
| `dash` | Whether a softer public relation is drawn with a dashed line |
| `scale` | Display weight |
| `u` | Public source URL supporting the relation |

Atlas v2 also reads three extension files:

- [`data/topics.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/topics.json): topic taxonomy, annotation model, and topic weights for each node.
- [`data/history.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/history.json): organisation history, matching rules, and Wikidata records; that source material is used under CC0.
- [`data/aliases_zh.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/aliases_zh.json): a mapping from node `id` to Chinese aliases used in search.

### Forum import rules

LessWrong and Alignment Forum data comes from the forums' public APIs: the same public data shown on profile and post pages.

- An existing person on the map who posts on either forum receives a `writes on` relation with post, comment, and karma counts and a profile-page source.
- Missing high-activity authors are added under fixed thresholds: Alignment Forum regulars need AF karma 300+ and 5+ AF posts; AI-topic authors need at least three AI posts with karma 100+; top LessWrong authors need total karma 8,000+, five posts with karma 100+, and five AI-topic posts. Low-activity accounts are intentionally excluded.
- When a forum post has no more than six authors, people already on the map may receive a `co-authored with` relation linked to that post.
- An account is matched to a named person only when the account publicly identifies itself. Pseudonymous authors remain under their public handles. Counts are snapshots from the import date.

### Principles

- Include public information only. Exclude contact details, private material, and family relations.
- Give every relation at least one public source that readers can inspect.
- Do not calculate paths between people or answer “who knows whom.”
- Keep visitor input in the browser. There is no backend model and no input is sent to a server.
- Inclusion, categories, and structural-community identifiers are not endorsements, criticism, reputation scores, or importance rankings.
- Honour deletion requests from represented people or their agents without conditions. See the full [inclusion policy](docs/INCLUSION.md).

### Contributing

You can file an add, correction, or removal request, or edit the JSON and open a pull request. Good first tasks include adding Chinese aliases, sourcing an organisation's founding year, and translating a short public description. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the workflow and field rules.

### Download the data

- [`nodes.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/nodes.json): people and organisation nodes.
- [`edges.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/edges.json): directed or undirected relations with labels and sources.
- [`topics.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/topics.json): node topic weights.
- [`history.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/history.json): organisation history and Wikidata provenance.
- [`aliases_zh.json`](https://raw.githubusercontent.com/Triciaaaaa/ai-risk-network/main/data/aliases_zh.json): Chinese aliases.

### Citation

See [`CITATION.cff`](CITATION.cff). GitHub also exposes it through “Cite this repository.”

### Licence

Code is licensed under the [MIT License](LICENSE). Data under `data/` is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) and requires attribution. Material identified as coming from Wikidata in `history.json` remains available under [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
