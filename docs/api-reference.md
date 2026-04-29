# API Reference

This page documents the public Python surface that is ready to use from
notebooks and scripts.

## Entry Point

```python
from cleanskate import Dataset

ds = Dataset(version="latest")
```

### `Dataset(...)`

Create a handle for a hosted or local cleanskate dataset.

Parameters:

- `version`: Dataset version to use. Defaults to `latest`.
- `base_dir`: Optional local dataset directory. When omitted, cleanskate uses a
  per-user cache directory.
- `manifest_url`: Remote manifest URL or URL template. Most users should leave
  this alone.
- `timeout`: Request timeout in seconds for manifest and table downloads.

## Loading Tables

Each loader returns a pandas `DataFrame`. Filters accept either a single value or
a list of values. List filters mean "one of these values."

### `load_events(...)`

Load one row per competition.

Useful filters:

- `event_id`
- `event_series`
- `event_level`
- `season`
- `event_label`

### `load_segments(...)`

Load one row per discipline segment within an event.

Useful filters:

- `event_id`
- `event_series`
- `event_level`
- `season`
- `event_label`
- `segment_id`
- `discipline`
- `segment_label`
- `is_team_event`

### `load_results(...)`

Load one row per skater or team in a segment.

Useful filters:

- `event_id`
- `event_series`
- `event_level`
- `season`
- `event_label`
- `segment_id`
- `segment_label`
- `discipline`
- `result_id`

By default, ID columns are hidden. Pass `include_ids=True` to keep all loaded
columns, or pass `columns=[...]` for an explicit subset.

### `load_standings(...)`

Load event-level standings.

Useful filters:

- `event_id`
- `event_series`
- `event_level`
- `season`
- `event_label`
- `discipline`
- `standing_type`

By default, ID columns are hidden. Pass `include_ids=True` to keep all loaded
columns, or pass `columns=[...]` for an explicit subset.

### `load_elements(...)`

Load one row per scored protocol element.

Useful filters:

- `event_id`
- `event_series`
- `event_level`
- `season`
- `event_label`
- `segment_id`
- `segment_label`
- `discipline`
- `element_family`
- `attempt_code`
- `clean_element`
- `fall`
- `fall_inferred`
- `invalid_element`
- `call_quarter`
- `call_underrotated`
- `call_downgraded`
- `call_edge_attention`
- `call_wrong_edge`
- `result_id`

By default, ID columns are hidden. Pass `include_ids=True` to keep all loaded
columns, or pass `columns=[...]` for an explicit subset.

### `load_program_components(...)`

Load one row per program component per skater-team per segment.

Useful filters:

- `event_id`
- `event_series`
- `event_level`
- `season`
- `event_label`
- `segment_id`
- `segment_label`
- `discipline`
- `result_id`

By default, ID columns are hidden. Pass `include_ids=True` to keep all loaded
columns, or pass `columns=[...]` for an explicit subset.

### `load_officials(...)`

Load one row per official identity.

Useful filters:

- `official_id`
- `nation`

By default, ID columns are hidden. Pass `include_ids=True` to keep all loaded
columns, or pass `columns=[...]` for an explicit subset.

### `load_segment_officials(...)`

Load one row per official assignment within a segment.

Useful filters:

- `event_id`
- `event_series`
- `event_level`
- `season`
- `event_label`
- `segment_id`
- `segment_label`
- `discipline`
- `official_id`
- `role`

By default, ID columns are hidden. Pass `include_ids=True` to keep all loaded
columns, or pass `columns=[...]` for an explicit subset.

## Cache And Manifest Helpers

### `prefetch(force=False)`

Download every table referenced by the current manifest into the local cache.
Use `force=True` to redownload files even when they already exist locally.

### `download_latest(force=False)`

Backward-compatible alias for `prefetch()`.

### `manifest()`

Return the current parsed dataset manifest. If remote fetching fails and a local
manifest exists, cleanskate falls back to the local copy.

### `available_tables()`

Return the table names that are available in the current local dataset
directory.

### `table_path(table_name)`

Return the local file path for a table, or `None` when the table is not
available locally.

## Detail Helpers

### `load_elements_for_result(result_row, include_ids=False)`

Load elements for one row returned by `load_results()`.

### `load_program_components_for_result(result_row, include_ids=False)`

Load program components for one row returned by `load_results()`.

### `expand_judge_scores(frame, column="judge_scores", prefix="judge_")`

Expand list-valued judge scores into numbered columns such as `judge_1`,
`judge_2`, and `judge_3`.

## Lower-Level Escape Hatch

### `load_table(table_name, filters=None, columns=None)`

Load any table by logical table name. This is useful when you need columns that
are not part of a loader's default public view.
