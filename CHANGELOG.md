# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### What's Changed

#### Fixed

- Fixed CI to run on PRs.

#### Added

- Added CI/CD pipeline for pre-commit, tests...

#### Changed

- Lowered the minimum required Python version to 3.8 and updated `pre-commit` minimum dependency.
- Added more tests for MacOS, Windows and Linux and various Python versions.
- Upgraded minimum python version from 3.8 to 3.9, to facilitate the use with numpy 2.x.y in development. Updated associated CI/CD pipeline.

#### Removed

- Removed the TODOS.md file and added the tasks to the issues.
- Removed dev dependencies for black and isort.

### New Contributors

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
