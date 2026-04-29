# Release Readiness

This is the practical checklist for getting `cleanskate` from useful local
package to something comfortable to publish and support.

## Current State

Already in good shape:

- Small public API centered on `Dataset`.
- Hosted-manifest download flow with local caching.
- Local dataset support for development and reproducible fixtures.
- Tests for filters, default columns, manifest fallback, stale cache refresh,
  helper lookups, and judge-score expansion.
- README, getting-started guide, data model notes, analysis caveats, and example
  notebooks.
- MIT license.

## Before First Public Release

Package metadata:

- Review `project.urls` and classifiers in `pyproject.toml` before publishing.
- Decide whether `0.1.0` is the first PyPI version or whether to publish an
  earlier pre-release.
- Keep `CHANGELOG.md` current as release scope changes.

Documentation:

- Add a short installation troubleshooting section for `pyarrow` and cache
  refresh issues.
- Document dataset snapshot naming and how long old snapshots will remain
  available.
- Add a provenance section explaining that source data comes from public skating
  results/protocol pages and that some fields are derived.
- Add a citation or acknowledgement note for users who publish analysis.
- Keep the notebooks runnable from a clean checkout.

Testing and quality:

- Add CI that runs tests on pull requests.
- Add at least one packaging check that builds the wheel and source
  distribution.
- Add linting or formatting once the preferred tool is chosen.
- Add a smoke test that imports the installed wheel, not only the editable
  checkout.

Dataset operations:

- Write down the process for publishing a new hosted manifest and table set.
- Preserve immutable dated manifests once published.
- Keep `latest` as a pointer, not as the only supported version.
- Add a simple validation checklist for row counts, required columns, and table
  relationships before publishing a new snapshot.

User experience:

- Decide what error messages should look like when the network is unavailable
  and no local cache exists.
- Consider a small CLI later for `prefetch`, cache location, and manifest
  inspection. The Python API is enough for the first release.
- Add issue templates once the repository is public enough to attract feedback.

## Nice To Have After Release

- Hosted documentation site generated from the Markdown docs.
- More cookbook examples for common analysis questions.
- Richer schema documentation, including dtypes and nullable fields.
- A versioned dataset changelog that is separate from the Python package
  changelog.
- Broader tests for real parquet snapshots, not only JSON fixtures.
