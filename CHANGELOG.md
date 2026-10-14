# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### What's Changed

#### Fixed

- The test workflow skipped all integration tests because they started before GeoServer was ready. It now waits for the GeoServer healthcheck (which was checking a path that always answers 404) and fails when GeoServer is unreachable instead of skipping. The user and user group deletion tests accept the 400 status returned by GeoServer 3.x.

#### Removed

- Removed pre-commit (`.pre-commit-config.yaml`, the dev dependency and `make pre-commit`). The linting workflow runs `ruff check` and `ruff format --check` instead, use `make format lint type` locally.

## 0.2.1 (2026-10-14)

### What's Changed

#### Changed

- Migrated the project from poetry to [uv](https://docs.astral.sh/uv/) (`uv.lock`, PEP 621 metadata, hatchling build backend). `__version__` is read from the installed package metadata, and `make patch|minor|major` bump the version with `uv version --bump`.
- Pushing a `v*` tag builds the distributions, checks the tag against the package version, publishes to PyPI with trusted publishing and creates the GitHub release. The test workflow builds the package and imports it from a bare wheel install.

## 0.2.0 (2025-01-27)

### What's Changed

#### Fixed

- Fix resource calls endpoints (#16).

#### Added

- Added CI/CD pipeline for pre-commit, tests, publishing to PyPI. Run tests and linter on PRs.

#### Changed

- Lowered the minimum required Python version to 3.8 and updated `pre-commit` minimum dependency.
- Added more tests for MacOS, Windows and Linux and various Python versions.
- Upgraded minimum python version from 3.8 to 3.9, to facilitate the use with numpy 2.x.y in development. Updated associated CI/CD pipeline.

#### Removed

- Removed the TODOS.md file and added the tasks to the issues.
- Removed dev dependencies for black and isort.

### New Contributors

- [@mcebria-hg](https://github.com/mcebria-hg)
- [@lkpanganiban](https://github.com/lkpanganiban)

## 0.1.0 (2024-06-12)

### What's Changed

#### Fixed

- Updated version to 0.0.1 to 0.1.0 for PyPI release.

#### Added

#### Changed

- Renamed and restructured some endpoints / methods to share a similar structure.
  (e.g. `get_workspace(workspace: str)` -> `get_workspace(name: str)`, `get_layer(layer: str)` -> `get_layer(name: str)`)
- Updated documentation and examples to reflect the changes.

#### Removed

### New Contributors

## 0.0.1 (2024-06-06)

### What's Changed

#### Fixed

#### Added

Initial release.

#### Changed

#### Removed

### New Contributors
