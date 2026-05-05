# Maintainer Notes

This page is for maintainers publishing `cleanskate` package releases or hosted
dataset snapshots.

## Package Release

### Preflight

Start from a clean working tree on `main`:

```bash
git status
git pull --ff-only
```

Run local checks:

```bash
pixi run clean-dist
pixi run test
pixi run build
pixi run check-dist
```

The build command writes artifacts to `dist/`, which is ignored by git.

### Version And Changelog

Before publishing:

- Confirm the version in `pyproject.toml`.
- Move the matching `CHANGELOG.md` section from `Unreleased` to the release
  date.
- Update [DATASET_CHANGELOG.md](../DATASET_CHANGELOG.md) if the hosted dataset
  snapshot changed as part of the release.
- Confirm the README, API reference, data model, and analysis notes match the
  release scope.
- Confirm CI is passing on `main`.

### TestPyPI

TestPyPI is the dry run for packaging and upload mechanics. It uses a separate
account, project namespace, and API token from real PyPI.

Before the first TestPyPI upload:

- Create a TestPyPI account at `https://test.pypi.org/`.
- Create a TestPyPI API token.
- Configure the token in `~/.pypirc` or enter it when `twine` prompts.

Rebuild immediately before upload:

```bash
pixi run clean-dist
pixi run build
pixi run check-dist
pixi run publish-testpypi
```

If TestPyPI rejects the upload because the version already exists, bump the
local version to a unique pre-release, post-release, or dev release, rebuild,
and try again.

TestPyPI does not mirror all dependencies, so install with PyPI as the extra
index:

```bash
python -m venv /tmp/cleanskate-testpypi-test
/tmp/cleanskate-testpypi-test/bin/python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  cleanskate
/tmp/cleanskate-testpypi-test/bin/python -c "from cleanskate import Dataset; print(Dataset.__name__)"
```

### PyPI

Preferred setup is PyPI Trusted Publishing from GitHub Actions. Until that is
configured, publish manually from a clean local checkout:

```bash
pixi run clean-dist
pixi run build
pixi run check-dist
pixi run publish-pypi
```

Do not upload from an old `dist/` directory. Rebuild immediately before
publishing.

### Tag The Release

After PyPI accepts the release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Then create a GitHub release from the tag and paste the relevant changelog
section.

### Post-Release Smoke Test

Install from PyPI in a new environment:

```bash
python -m venv /tmp/cleanskate-release-test
/tmp/cleanskate-release-test/bin/python -m pip install cleanskate
/tmp/cleanskate-release-test/bin/python -c "from cleanskate import Dataset; print(Dataset.__name__)"
```

## Dataset Release

For user-facing guidance on choosing a snapshot, see
[Dataset versions](./dataset-operations.md).

### Versioning Policy

Use two kinds of manifests:

- `latest.json`: a moving pointer for exploratory analysis.
- Dated manifests: immutable snapshots for reproducible analysis.

Dated manifests should use a date-stamped version:

```text
2026-04-12
```

Once published, a dated manifest should remain available. If a correction is
needed, publish a new dated manifest and move `latest.json` to that new version.

### Snapshot Checklist

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

### Required Tables

Hosted snapshots should include:

- `events`
- `segments`
- `results`
- `standings`
- `officials`
- `segment_officials`
- `elements`
- `program_components`

### Manifest Expectations

Each manifest table entry should include:

- `url`
- `filename`
- `format`

Parquet is preferred for hosted tables. JSON remains useful for small local test
fixtures.

### Publishing Flow

1. Build the normalized tables.
2. Validate the tables using the snapshot checklist.
3. Export the snapshot bundle, including manifests and release metadata.
4. Upload table files to the hosted dataset location.
5. Upload a dated immutable manifest.
6. Update `latest.json` only after the dated manifest is confirmed.
7. Run a fresh `Dataset(version="latest").prefetch(force=True)` smoke test.
8. Add a dataset changelog entry or release note describing coverage changes,
   schema changes, and known caveats.

### Snapshot Metadata

The snapshot export flow should emit lightweight metadata alongside each
manifest. At minimum, that metadata should include:

- `version`
- `updated_at`
- row counts for every public table

This makes it easier to:

- write release notes quickly
- compare snapshots at a glance
- sanity-check that a release contains the expected public data

### Release-Note Helper

The backend repo includes a helper that turns snapshot metadata plus unresolved
`EVENTS.yml` entries into a Markdown release-note skeleton:

```bash
python 10_prepare_dataset_release.py \
  --metadata /tmp/cleanskate_snapshot/latest-metadata.json
```

You can paste the generated output into
[`DATASET_CHANGELOG.md`](../DATASET_CHANGELOG.md) and then edit the coverage,
schema, and quality sections with the specific human-facing notes for that
snapshot.
