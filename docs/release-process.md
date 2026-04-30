# Release Process

This is the checklist for publishing a Python package release.

## Preflight

Start from a clean working tree on `main`:

```bash
git status
git pull --ff-only
```

Run local checks:

```bash
pixi run test
pixi run build
pixi run check-dist
```

The build command writes artifacts to `dist/`, which is ignored by git.

## Version And Changelog

Before publishing:

- Confirm the version in `pyproject.toml`.
- Move the matching `CHANGELOG.md` section from `Unreleased` to the release
  date.
- Confirm the README, API reference, and release readiness docs match the
  release scope.
- Confirm CI is passing on `main`.

## Publish To PyPI

Preferred setup is PyPI Trusted Publishing from GitHub Actions. Until that is
configured, publish manually from a clean local checkout:

```bash
pixi run build
pixi run twine upload dist/*
```

Do not upload from an old `dist/` directory. Rebuild immediately before
publishing.

## Tag The Release

After PyPI accepts the release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Then create a GitHub release from the tag and paste the relevant changelog
section.

## Post-Release Smoke Test

Install from PyPI in a new environment:

```bash
python -m venv /tmp/cleanskate-release-test
/tmp/cleanskate-release-test/bin/python -m pip install cleanskate
/tmp/cleanskate-release-test/bin/python -c "from cleanskate import Dataset; print(Dataset.__name__)"
```

For a dataset release, also smoke-test the hosted manifest:

```python
from cleanskate import Dataset

ds = Dataset(version="latest")
ds.prefetch(force=True)
print(ds.available_tables())
```
