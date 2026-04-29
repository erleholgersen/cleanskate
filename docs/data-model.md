# Data Model

`cleanskate` is intentionally table-first. The package does not try to hide the
underlying data model behind a heavy abstraction layer.

## Public Tables

### `events`

One row per competition.

Common columns:

- `event_label`
- `event_series`
- `event_level`
- `competition_name`
- `season`
- `location`
- `venue`
- `start_date`
- `end_date`

### `segments`

One row per discipline segment within an event.

Common columns:

- `event_label`
- `discipline`
- `segment_name`
- `segment_label`
- `segment_order`
- `result_count`

### `results`

One row per skater or team per segment.

Common columns:

- `rank`
- `name`
- `noc`
- `starting_number`
- `total_segment_score`
- `total_element_score`
- `total_program_component_score`
- `total_deductions`
- `reported_falls`

### `standings`

One row per event-level standing entry.

Common columns:

- `discipline`
- `standing_type`
- `rank`
- `name`
- `noc`
- `total_score`
- `segment_1_label`
- `segment_1_score`
- `segment_2_label`
- `segment_2_score`

### `elements`

One row per scored element row in a protocol.

Common columns:

- `element_number`
- `element_code`
- `attempt_code`
- `element_family`
- `scored_element`
- `clean_element`
- `fall`
- `fall_inferred`
- `invalid_element`
- `call_quarter`
- `call_underrotated`
- `call_downgraded`
- `call_edge_attention`
- `call_wrong_edge`
- `info_flags`
- `base_value`
- `bonus_points`
- `goe`
- `panel_score`
- `judge_scores`

### `program_components`

One row per component per skater-team per segment.

Common columns:

- `component_name`
- `factor`
- `average`
- `judge_scores`

### `officials`

One row per official identity.

Common columns:

- `name`
- `nation`

### `segment_officials`

One row per official assignment within a segment.

Common columns:

- `event_label`
- `segment_label`
- `role`
- `panel_position`
- `name`
- `nation`

## Naming Conventions

Some fields are raw-ish, some are direct derivations, and some are broader
interpretations.

### Raw-ish source fields

- `info_flags`
- `judge_scores`

### Direct call-derived fields

- `call_quarter`
- `call_underrotated`
- `call_downgraded`
- `call_edge_attention`
- `call_wrong_edge`

### Broader interpreted fields

- `scored_element`
- `invalid_element`
- `clean_element`
- `fall`
- `fall_inferred`

## Important Element Semantics

### `scored_element`

This means the row had usable judge marks. It is not the same thing as "rules
valid."

### `invalid_element`

This reflects an explicit invalidation marker such as `*` in the protocol.

### `clean_element`

This is currently defined as:

- a scored element row
- with no raw `info_flags`
- with no explicit or inferred fall assigned to the element

If the segment reports falls but they cannot be assigned confidently to specific
elements, `clean_element` can be missing rather than `True` or `False`.

### `fall`

`fall` is the best available element-level fall assignment.

It can be:

- explicit from protocol annotations
- inferred conservatively in a narrow set of older protocols
- missing when falls are reported at the segment level but cannot be assigned to
  a specific element confidently

## Design Philosophy

The package aims to be:

- pandas-first
- explicit about derived fields
- conservative about noisy protocol interpretation
- simple enough that users can still inspect the underlying columns themselves
