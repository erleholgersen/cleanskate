# Changelog

All notable changes to `cleanskate` will be documented here.

## 0.1.0 - Unreleased

Initial public package preparation:

- Add the `Dataset` API for loading hosted or local score tables as pandas data
  frames.
- Support automatic table downloads, manifest refreshes, local caching, and
  cache fallback when the network is unavailable.
- Add public loaders for events, segments, results, standings, officials,
  segment officials, elements, and program components.
- Add notebook-friendly filters for common fields such as season, event series,
  discipline, segment label, element family, attempt code, and call flags.
- Add example notebooks and Markdown documentation for getting started, the data
  model, analysis caveats, API usage, and release readiness.
- Add CI for tests, package builds, metadata checks, and installed-wheel smoke
  tests.
- Add provenance, citation, troubleshooting, and dataset publishing guidance.
- Add GitHub issue templates for bugs, data issues, and feature requests.
- Add a release process checklist for PyPI publishing and post-release smoke
  tests.
- Add TestPyPI release instructions and reusable Pixi publish tasks.
