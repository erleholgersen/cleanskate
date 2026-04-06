# cleanskate

`cleanskate` is a Python package for loading figure skating scores
into pandas data frames.

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

You can also point the loader at a local dataset directory:

```python
from cleanskate import Dataset

dataset = Dataset(base_dir="/path/to/local/dataset")
segments = dataset.load_segments()
```

The loader fetches missing tables automatically on first use, so users do not
need to call a separate download step. `prefetch()` is still available when you
want to warm the local cache explicitly.
