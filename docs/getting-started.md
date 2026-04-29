# Getting Started

## Basic Workflow

`cleanskate` is built around one main entry point:

```python
from cleanskate import Dataset

ds = Dataset(version="latest")
```

From there, you load one or more public tables into pandas:

```python
events = ds.load_events()
segments = ds.load_segments()
results = ds.load_results()
standings = ds.load_standings()
elements = ds.load_elements()
program_components = ds.load_program_components()
officials = ds.load_officials()
segment_officials = ds.load_segment_officials()
```

The package downloads missing files automatically and caches them locally.

## Choosing a Dataset Version

For most users, `latest` is the right starting point:

```python
ds = Dataset(version="latest")
```

If you want to pin analysis to a specific published snapshot:

```python
ds = Dataset(version="2026-04-12-segment-label-cleanup")
```

## Useful Filtering Patterns

Loaders support pandas-friendly filters directly.

### By event family

```python
worlds = ds.load_events(event_series="Worlds")
gp_results = ds.load_results(event_series="Grand Prix")
```

### By season or label

```python
season_results = ds.load_results(season="2025-2026")
worlds_2026 = ds.load_results(event_label="Worlds 2026")
```

### By segment or discipline

```python
men_sp = ds.load_results(segment_label="Men SP")
women = ds.load_segments(discipline="Women")
```

### By element type

```python
jumps = ds.load_elements(element_family="Jump")
triple_axels = ds.load_elements(attempt_code="3A")
```

## Working With Element Calls

The `elements` table includes both raw and derived call fields.

Examples:

```python
clean_axels = ds.load_elements(
    attempt_code=["2A", "3A"],
    clean_element=True,
)

rotation_issues = ds.load_elements(
    call_quarter=True,
)
```

The most important fields are:

- `info_flags`: raw-ish source call field
- `call_quarter`
- `call_underrotated`
- `call_downgraded`
- `call_edge_attention`
- `call_wrong_edge`
- `fall`
- `fall_inferred`
- `clean_element`

## Caching

Downloaded files are cached locally per dataset version. Repeated calls on the
same `Dataset` object also reuse in-memory table caches, so notebook workflows
stay fast after the first load.

If you want to download everything up front:

```python
ds.prefetch()
```

If you want to force a refresh:

```python
ds.prefetch(force=True)
```
