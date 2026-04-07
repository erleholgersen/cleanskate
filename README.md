# ⛸️ cleanskate 

**cleanskate** is a Python package for accessing figure skating scores as pandas data frames.

## Example

```python
from cleanskate import Dataset

dataset = Dataset(version="latest")

events = dataset.load_events()
results = dataset.load_results()
elements = dataset.load_elements()
```

The loader also supports a few pandas-friendly filters that are useful in
notebooks:

```python
from cleanskate import Dataset

dataset = Dataset()

worlds_events = dataset.load_events(event_series="Worlds")
season_results = dataset.load_results(season="2025-2026")
men_short_program = dataset.load_elements(segment_label="Men SP")
jumps_at_worlds = dataset.load_elements(
    event_series="Worlds",
    element_family="Jump",
)
grand_prix_women = dataset.load_results(
    event_series="Grand Prix",
    discipline="Women",
)
```

All loader filters accept either a single value or a list of values. Lists use
"one of these values" semantics:

```python
from cleanskate import Dataset

dataset = Dataset()

senior_mens_jumps = dataset.load_elements(
    event_level=["Senior", "Mixed"],
    discipline="Men",
    element_family="Jump",
)

triple_axel_attempts = dataset.load_elements(
    attempt_code="3A",
)

non_clean_jump_attempts = dataset.load_elements(
    event_level="Senior",
    attempt_code=["3A", "4T", "4S"],
    clean_element=False,
)
```

The current recommended public filters are:

- `season`
- `event_series`
- `event_level`
- `event_label`
- `segment_label`
- `discipline`
- `element_family`
- `attempt_code`
- `clean_element`

Lower-level IDs like `event_id`, `segment_id`, and `result_id` are still
available for power users, but most notebook workflows should not need them.

You can also point the loader at a local dataset directory:

```python
from cleanskate import Dataset

dataset = Dataset(base_dir="/path/to/local/dataset")
segments = dataset.load_segments()
```

The loader fetches missing tables automatically on first use, so users do not
need to call a separate download step. `prefetch()` is still available when you
want to warm the local cache explicitly.

## Related work

There are several related projects.

- [BuzzFeed data parsers](https://github.com/BuzzFeedNews/figure-skating-scores/tree/master)
- [BuzzFeed judge bias analysis](https://www.buzzfeednews.com/article/johntemplon/the-edge)
- 
