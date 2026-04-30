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
- Follow the release process checklist for build, publish, tag, and smoke-test
  steps.

Documentation:

- Review installation troubleshooting for `pyarrow` and cache refresh issues.
- Review dataset snapshot naming and retention policy.
- Review provenance and citation guidance.
- Keep the notebooks runnable from a clean checkout.

Testing and quality:

- Watch the new CI workflow on the first pushed branch after this checklist
  update.
- Add linting or formatting once the preferred tool is chosen.

Dataset operations:

- Exercise the documented dataset publishing flow on the next snapshot.
- Keep [DATASET_CHANGELOG.md](../DATASET_CHANGELOG.md) current as snapshots are published.

User experience:

- Decide what error messages should look like when the network is unavailable
  and no local cache exists.
- Consider a small CLI later for `prefetch`, cache location, and manifest
  inspection. The Python API is enough for the first release.
- Review issue templates after the first few external reports.

## Nice To Have After Release

- Hosted documentation site generated from the Markdown docs.
- More cookbook examples for common analysis questions.
- Richer schema documentation, including dtypes and nullable fields.
- A versioned dataset changelog that is separate from the Python package
  changelog.
- Broader tests for real parquet snapshots, not only JSON fixtures.
