# AI risk fund & member network

An interactive map of who funds, runs, advises and co-authors with whom in the AI existential-risk world: funders, safety organisations, frontier-lab leadership, researchers, policy people and writers, plus the organisations that connect them. Every relation carries a public source URL.

**Live map:** https://triciaaaaa.github.io/ai-risk-network/

- Circles are people, squares are organisations. Colour = group: research / safety org / funder / lab / policy / media.
- Orange lines are money; grey lines are positions (employed by, board of, founded…); blue lines are co-authorship and alliances.
- Teal lines are forum activity: who writes on LessWrong and the Alignment Forum.
- Click a node to see all of its relations with sources. Search by name. Zoom in to reveal the long tail (the overview only draws nodes with 4+ relations).

## What is (and is not) in here

Only public facts: public roles and affiliations, public grants and investments, public co-authorship, and public statements of alliance or opposition, each with the page it came from. No contact details, no private assessments, no family relations. If you are listed and want something corrected or removed, open an issue or a PR; removal requests are honoured without discussion.

## Forum activity (LessWrong / Alignment Forum)

Read from the forums' own public API (the data their profile and post pages show). Three things come from it:

- Anyone already on the map who posts there gets a `writes on` link to the forum, with post, comment and karma counts and the profile page as source.
- Star authors who were missing are added: Alignment Forum regulars (AF karma 300+ and 5+ AF posts), authors of three or more AI posts at 100+ karma, and top LessWrong authors (karma 8,000+, five posts at 100+ karma, five on AI). Low-activity accounts are left out on purpose.
- Two people on the map who share a forum post (six authors or fewer) get a `co-authored with` link to that post.

An account is tied to a named person only when the account says so itself: the display name is the name, the handle spells it, or the public bio or the person's own site states it. Pseudonymous authors appear under the handle they publish under. Counts are a snapshot of the public profile on the import date.

## Contributing (pull requests welcome)

The map is generated from two JSON files:

- `data/nodes.json`: one object per person or organisation. Fields: `id` (kebab-case), `name`, `type` (`person` | `org`), `cluster`, and optionally `affil`, `focus`, `writings` (short public descriptions) and `url` (a public page).
- `data/edges.json`: one object per relation. Fields: `s` (source id), `t` (target id), `label` (for example `funds · $1.2M 2025`), `arrow` (`1->2` when directed, else empty), `dash` (`true` for soft ties such as ally / opponent), `u` (source URL; required for anything a reader might dispute).

To add or fix something: edit the JSON, run `python validate.py && python build.py`, and open a pull request. CI runs the same checks, and merged PRs rebuild `index.html` automatically. Rules of thumb: one public source per relation, public figures and organisations only, no personal contact information.

## Licence

Code: MIT. Data: CC BY 4.0. Reuse freely with attribution.
