https://keepachangelog.com/en/

## [2.0.0] - 2024-11-25

### Changed

- major code refactoring and cleanup to make the whole code more modularized and readable
- move add-on's panel location to File Browser. it seems like a more appropriate place
- pre-build operator parameters instead of generating them on every `draw` call

### Added

- Save operators resulting path preview in the descriptions
- Delete Data operator
- Help operator which opens README file
- on/off Files Openers toggle

## [1.1.0] - 2024-11-11

### Added

- Import & Export Templates to TOML files

## [1.0.0] - 2024-10-27

Save Incremental Advanced initial features. see #1.0.0 README file for the full description.

### Added

- "Save " operator with multipart numerical versioning scheme with configurable separators
  à la [Semantic Versioning](https://semver.org/).
- configurable blend-file persistent "Save Templates" data.
- 3D Viewport Sidebar panel with the add-on's UI.
- various supporting features.