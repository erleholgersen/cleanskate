# Dataset Operations

This page documents the intended process for publishing hosted cleanskate
dataset snapshots.

## Versioning Policy

Use two kinds of manifests:

- `latest.json`: a moving pointer for exploratory analysis.
- Dated manifests: immutable snapshots for reproducible analysis.

Dated manifests should use a stable, descriptive version such as:

```text
2026-04-12-segment-label-cleanup
```

Once published, a dated manifest should remain available. If a correction is
needed, publish a new dated manifest and move `latest.json` to that new version.

## Snapshot Checklist

Before publishing a new snapshot:

- Confirm every expected table exists.
- Confirm every table has the required public columns.
- Confirm foreign-key relationships line up:
  - `segments.event_id` values exist in `events.event_id`.
  - `results.segment_id` values exist in `segments.segment_id`.
  - `elements.result_id` values exist in `results.result_id`.
  - `program_components.result_id` values exist in `results.result_id`.
  - `segment_officials.segment_id` values exist in `segments.segment_id`.
  - `segment_officials.official_id` values exist in `officials.official_id`.
- Record row counts for each table.
- Spot-check at least one event from each major event family included in the
  snapshot.
- Confirm the manifest `updated_at` value changed.
- Confirm `Dataset(version="<snapshot>")` can prefetch and load all tables.
- Confirm `Dataset(version="latest")` resolves to the intended release after
  updating `latest.json`.

## Required Tables

Hosted snapshots should include:

- `events`
- `segments`
- `results`
- `standings`
- `officials`
- `segment_officials`
- `elements`
- `program_components`

## Manifest Expectations

Each manifest table entry should include:

- `url`
- `filename`
- `format`

Parquet is preferred for hosted tables. JSON remains useful for small local test
fixtures.

## Publishing Flow

1. Build the normalized tables.
2. Validate the tables using the snapshot checklist.
3. Upload table files to the hosted dataset location.
4. Upload a dated immutable manifest.
5. Update `latest.json` only after the dated manifest is confirmed.
6. Run a fresh `Dataset(version="latest").prefetch(force=True)` smoke test.
7. Add a dataset changelog entry or release note describing coverage changes,
   schema changes, and known caveats.
