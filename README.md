# ⛸️ cleanskate

`cleanskate` is a Python package for loading figure skating scores as pandas data
frames. The package covers overall results, judge information, program component
scores, and per-element scores for international events from the `2018-2019`
season onward.

The current dataset covers major international events, including:

- Olympics
- Worlds
- Junior Worlds
- Europeans
- Four Continents
- Grand Prix
- Grand Prix Final
- Junior Grand Prix
- much of the Challenger Series

The dataset may be expanded in the future. Feel free to open an issue if you
notice anything missing.

## Installation

```bash
pip install cleanskate
```

For local development:

```bash
pip install -e .
```

## Quick Start

```python
from cleanskate import Dataset

ds = Dataset(version="latest")

events = ds.load_events()
results = ds.load_results()
elements = ds.load_elements()
```

Tables are downloaded automatically on first use and cached locally. You do not
need to call a separate download command.

## Common Filters

All loader filters accept either a single value or a list of values. Lists use
"one of these values" semantics.

```python
from cleanskate import Dataset

ds = Dataset()

worlds_events = ds.load_events(event_series="Worlds")
season_results = ds.load_results(season="2025-2026")
women_segments = ds.load_segments(discipline="Women")
triple_axels = ds.load_elements(attempt_code="3A")

senior_jump_attempts = ds.load_elements(
    event_level="Senior",
    element_family="Jump",
)

non_clean_jumps = ds.load_elements(
    attempt_code=["3A", "4T", "4S"],
    clean_element=False,
)
```

Recommended public filters:

- `season`
- `event_series`
- `event_level`
- `event_label`
- `segment_label`
- `discipline`
- `element_family`
- `attempt_code`
- `clean_element`

Lower-level IDs like `event_id`, `segment_id`, and `result_id` are also
available for power users.

## Local Datasets

You can point `Dataset` at a local directory instead of the hosted snapshot:

```python
from cleanskate import Dataset

ds = Dataset(base_dir="/path/to/local/dataset")
segments = ds.load_segments()
```

`prefetch()` is available if you want to warm the cache explicitly:

```python
ds.prefetch()
```

## Example Notebooks

The repository currently includes:

- [Quick start notebook](./examples/quick_start.ipynb)
- [Judge nationality patterns notebook](./examples/judge_nationality_patterns.ipynb)

## Documentation

Additional docs:

- [Getting started](./docs/getting-started.md)
- [API reference](./docs/api-reference.md)
- [Data model](./docs/data-model.md)
- [Dataset operations](./docs/dataset-operations.md)
- [Dataset changelog](./DATASET_CHANGELOG.md)
- [Provenance and citation](./docs/provenance.md)
- [Analysis notes](./docs/analysis-notes.md)
- [Release process](./docs/release-process.md)
- [Release readiness](./docs/release-readiness.md)


## Related Work

- [BuzzFeed data parsers](https://github.com/BuzzFeedNews/figure-skating-scores/tree/master)
- [BuzzFeed judge bias analysis](https://www.buzzfeednews.com/article/johntemplon/the-edge)
