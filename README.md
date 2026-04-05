# cleanskate

`cleanskate` is a user-facing Python package for loading figure skating scores
into pandas data frames.

## Example

```python
from cleanskate import Dataset

dataset = Dataset(version="latest")

events = dataset.load_events()
results = dataset.load_results()
elements = dataset.load_elements()
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

## Next Data Step

The main missing piece is uploading a first dataset manifest and table files to
the `cleanskate` bucket. Once those objects exist, the package scaffold here can
download and cache them.
