# Dataset Versions

`cleanskate` publishes score data as hosted dataset snapshots. Most users only
need to decide whether they want the moving `latest` snapshot or a fixed dated
snapshot.

## Which Version To Use

Use `latest` when you are exploring:

```python
from cleanskate import Dataset

ds = Dataset(version="latest")
```

`latest` points to the newest hosted dataset. It is convenient in notebooks, but
it can change when coverage or parsing corrections are published.

Use a dated snapshot when you want an analysis to be reproducible:

```python
ds = Dataset(version="2026-04-12")
```

Dated snapshots are intended to remain available after publication. If the data
needs a correction, the corrected data should be published as a new dated
snapshot, and `latest` should move to that new snapshot.

## Reading A Snapshot Version

Dataset versions are date-stamped:

```text
YYYY-MM-DD
```

The date identifies the hosted dataset snapshot, not the Python package version.
For example, `cleanskate==0.1.0` can read different dataset snapshots if they
share the same public schema.

## Recording A Snapshot

For work you expect to revisit, record both:

- the `cleanskate` package version
- the dataset snapshot version

Example:

```text
cleanskate package: 0.1.0
cleanskate dataset snapshot: 2026-04-12
```

The important part is knowing which package and dataset produced the results.

## Cache Behavior

Downloaded files are cached locally per dataset version. Repeated calls with the
same version use the local files after the first download.

`Dataset(version="latest")` checks the hosted manifest and refreshes stale
cached files when `latest` moves. If a notebook seems to be using old data, force
a refresh:

```python
ds = Dataset(version="latest")
ds.prefetch(force=True)
```
