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
pixi run clean-dist
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
- Update [DATASET_CHANGELOG.md](../DATASET_CHANGELOG.md) if the hosted dataset
  snapshot changed as part of the release.
- Confirm the README, API reference, and release readiness docs match the
  release scope.
- Confirm CI is passing on `main`.

## Publish To TestPyPI

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

If TestPyPI rejects the upload because `0.1.0` already exists, bump the local
version to a unique pre-release or dev release such as `0.1.0rc1` or
`0.1.0.dev1`, rebuild, and try again.

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

## Publish To PyPI

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
