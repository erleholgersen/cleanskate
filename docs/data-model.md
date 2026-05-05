# Data Model

`cleanskate` keeps the data close to the shape of the scoring protocol. The
main unit is a table, and the public loaders return pandas data frames with the
columns most people need first. Identifier and source columns are still there
when you ask for them with `include_ids=True` or an explicit `columns=[...]`.

## Public Tables

| Table | Description |
| --- | --- |
| events | Competitions. |
| segments | Discipline segments within events. |
| results | Skater or team results within segments. |
| standings | Event-level placements. |
| elements | Scored element rows from detailed protocols. |
| program_components | Program component score rows. |
| officials | Official identities. |
| segment_officials | Official assignments within segments. |

## Shared Context Columns

Most tables carry a small amount of repeated context so they are useful on their
own in a notebook.

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Human-readable event name, such as `Worlds 2026`. | |
| `event_series` | Event family, such as `Worlds` or `Grand Prix`. | Normalized by `cleanskate`. |
| `event_level` | Broad level, such as `Senior`, `Junior`, or `Mixed`. | `Mixed` is used where an event contains more than one level. |
| `season` | Season label, such as `2025-2026`. | |
| `segment_label` | Compact segment label, such as `Men FS`. | Normalized for readability. |
| `name` | Skater, team, or official display name. | |
| `noc` | Skater/team nation code. | |

## Table Columns

The tables below list the default columns returned by the public loaders. Extra
identifier and source columns are available with `include_ids=True`.

### Events

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Short display label, such as `Worlds 2026`. | |
| `event_series` | Event family. | |
| `event_level` | Senior, junior, mixed, or another broad level. | Derived from event metadata. |
| `competition_name` | Full competition title from the source. | |
| `season` | Season label, such as `2025-2026`. | |
| `location` | Source location text. | |
| `venue` | Venue name when available. | |
| `start_date` | Event start date when available. | |
| `end_date` | Event end date when available. | |

### Segments

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Event display label. | |
| `event_series` | Event family. | |
| `event_level` | Event level. | |
| `discipline` | Segment discipline, such as `Men`, `Women`, `Pairs`, or `Ice Dance`. | |
| `segment_name` | Source segment name. | |
| `segment_label` | Compact display label, such as `Men FS`. | |
| `is_team_event` | Whether the segment belongs to a team event. | |
| `base_discipline` | Discipline without team-event wrapping. | |
| `result_count` | Number of result rows found for the segment. | Useful for coverage checks. |
| `segment_order` | Segment order within the event/discipline. | Numeric when it can be determined. |

### Results

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Event display label. | |
| `event_series` | Event family. | |
| `event_level` | Event level. | |
| `segment_label` | Segment display label, such as `Women SP`. | |
| `rank` | Segment rank. | |
| `name` | Skater or team name. | |
| `noc` | Nation code. | |
| `starting_number` | Starting order number when available. | |
| `total_segment_score` | Total score for the segment. | Usually TES + PCS - deductions. |
| `total_element_score` | Technical element score. | Often abbreviated TES. |
| `total_program_component_score` | Program component score. | Often abbreviated PCS. |
| `total_deductions` | Total deductions shown for the segment. | Includes fall deductions when reported. |
| `reported_falls` | Number of falls reported at result/segment level. | This is not always enough to identify the exact element. |
| `element_base_value_sum` | Sum of parsed element base values. | Derived from the element rows. |
| `element_panel_score_sum` | Sum of parsed element panel scores. | Derived from the element rows. |
| `program_component_score_factored` | Sum of factored component scores. | Derived from component rows when available. |
| `deduction_detail` | Source deduction detail text or parsed structure. | Source-specific. |

### Standings

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Event display label. | |
| `event_series` | Event family. | |
| `event_level` | Event level. | |
| `season` | Season label, such as `2025-2026`. | |
| `discipline` | Standing discipline, such as `Men`. | |
| `standing_name` | Source/display name for the standing, such as `Men Final`. | |
| `standing_type` | Standing type. | Often `Final`; may vary by event. |
| `rank` | Event-level rank. | |
| `name` | Skater or team name. | |
| `noc` | Nation code. | |
| `total_score` | Total standing score. | Usually sum of segment scores. |
| `segment_1_label` | First segment label when the standing breaks out segment scores. | |
| `segment_1_score` | First segment score. | |
| `segment_1_rank` | First segment rank. | |
| `segment_2_label` | Second segment label for two-segment standings. | |
| `segment_2_score` | Second segment score. | |
| `segment_2_rank` | Second segment rank. | |

### Elements

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Event display label. | |
| `event_series` | Event family. | |
| `event_level` | Event level. | |
| `segment_label` | Segment display label, such as `Men FS`. | |
| `name` | Skater or team name. | |
| `noc` | Nation code. | |
| `element_number` | Element order in the protocol. | |
| `element_code` | Full protocol element code. | Includes calls such as `<`, `q`, `e`, or `*`. |
| `attempt_code` | Cleaned attempted element code. | Derived; for example, `3A<` has attempt code `3A`. |
| `element_family` | Broad element family. | Derived; examples include `Jump`, `Spin`, `Step`, `Lift`. |
| `scored_element` | Whether the row has usable scoring values. | This is not the same as rules-valid. |
| `clean_element` | Convenience flag for a scored row with no calls or assigned fall. | Missing when the parser cannot safely decide. |
| `fall` | Best available element-level fall assignment. | Explicit when possible; sometimes inferred conservatively. |
| `fall_inferred` | Whether `fall` was inferred rather than read directly. | See [fall assignment](#fall-assignment). |
| `invalid_element` | Whether the protocol marks the element invalid. | Usually from an explicit `*`. |
| `call_quarter` | Quarter-under call. | Derived from protocol call markers. |
| `call_underrotated` | Under-rotated call. | Derived from protocol call markers. |
| `call_downgraded` | Downgrade call. | Derived from protocol call markers. |
| `call_edge_attention` | Edge attention call. | Usually `!`. |
| `call_wrong_edge` | Wrong-edge call. | Usually `e`. |
| `info_flags` | Raw-ish protocol call text. | Useful for inspecting the original marker bundle. |
| `base_value` | Base value for the element. | |
| `bonus_points` | Bonus value shown separately by the source. | Numeric; often `0`. |
| `second_half_bonus` | Whether the element received second-half bonus treatment. | Derived from source scoring fields. |
| `goe` | Final grade of execution value. | |
| `panel_score` | Final panel score for the element. | Usually base value plus GOE and bonuses. |
| `judge_scores` | List of individual judge GOE marks. | Use `expand_judge_scores()` for judge-number columns. |

### Program Components

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Event display label. | |
| `event_series` | Event family. | |
| `event_level` | Event level. | |
| `segment_label` | Segment display label, such as `Pairs FS`. | |
| `name` | Skater or team name. | |
| `noc` | Nation code. | |
| `component_name` | Program component name, such as `Composition`, `Presentation`, or `Skating Skills`. | |
| `factor` | Component factor. | |
| `average` | Averaged component mark. | |
| `judge_scores` | List of individual judge component marks. | Use `expand_judge_scores()` for judge-number columns. |

### Officials

| Column | Description | Notes |
| --- | --- | --- |
| `name` | Official display name. | Source formatting can vary across events. |
| `nation` | Official nation or affiliation. | `ISU` appears for some technical officials. |

### Segment Officials

| Column | Description | Notes |
| --- | --- | --- |
| `event_label` | Event display label. | |
| `segment_label` | Segment display label, such as `Women FS`. | |
| `role` | Panel role, such as `Referee`, `Judge No.1`, or `Technical Controller`. | |
| `panel_position` | Numeric judge position when applicable. | Usually populated for judges, not all officials. |
| `name` | Official display name. | |
| `nation` | Official nation or affiliation. | |

## Identifier And Source Columns

Default loaders hide internal identifiers because they tend to clutter the first
view of a table. They are useful when joining tables or tracing rows back to
source pages.

| Column pattern | Usually appears on | Description |
| --- | --- | --- |
| `event_id` | Most tables | Stable event identifier used for joins. |
| `segment_id` | Segment-level detail tables | Stable segment identifier used for joins. |
| `result_id` | Results, elements, components | Stable result-row identifier used for joins. |
| `element_id` | Elements | Stable element-row identifier. |
| `program_component_id` | Program components | Stable component-row identifier. |
| `official_id` | Officials and assignments | Stable official identifier. |
| `segment_official_id` | Segment official assignments | Stable assignment identifier. |
| `*_source_url` or `source_url` | Source-backed tables | URL used while parsing, when retained. |

## Naming Conventions

Some fields are close to the source page. Others are parsed interpretations. The
distinction matters most in the `elements` table.

| Kind | Columns | How to read them |
| --- | --- | --- |
| Source-like fields | `element_code`, `info_flags`, `base_value`, `goe`, `panel_score`, `judge_scores` | Parsed from protocol values with minimal interpretation. |
| Direct call fields | `call_quarter`, `call_underrotated`, `call_downgraded`, `call_edge_attention`, `call_wrong_edge`, `invalid_element` | Boolean flags derived from explicit call markers. |
| Convenience fields | `attempt_code`, `element_family`, `scored_element`, `clean_element`, `fall`, `fall_inferred` | Added to make common analysis easier; inspect the source-like fields when the distinction matters. |

## Element Semantics

### scored_element

`scored_element` means the row had usable scoring values. An invalidated element
can still have a row in the protocol, so this is not a general rules-valid flag.

### invalid_element

`invalid_element` reflects an explicit invalidation marker such as `*` in the
protocol.

### clean_element

`clean_element` is a practical filter, not a statement about the entire
performance. It is currently true when an element row is scored and has no raw
`info_flags` and no explicit or inferred fall assigned to that element.

If a segment reports falls but the parser cannot assign them confidently to
specific elements, `clean_element` can be missing rather than `True` or `False`.

### Fall Assignment

`fall` is the best available element-level fall assignment.

It can be:

- explicit from protocol annotations
- inferred when the result reports a fall deduction and the parser can assign
  that fall to a specific element
- missing when falls are reported at the segment level but cannot be assigned to
  a specific element confidently

When `fall_inferred` is `True`, the package has filled in an element-level fall
from the reported deduction rather than copying an explicit element marker. If
one assignment matters for your analysis, it is worth checking the source
protocol.
