### Changelog

### NEXT

* Enforce required nodes/fields at write time in class `to_xml` (raises on missing required Source/Projections/Geometries unless auto-filled).
* Auto-fill minimal IDs for non-multipatch fixtures/truss/support/video/projector when missing (`FixtureID="0"`, `FixtureIDNumeric=0`, fixtures also `UnitNumber=0`).
* Preserve `UserData/Data` payload content (text/children) on round-trip.
* Default `Gobo` rotation to `0.0` to avoid invalid `None` serialization.
* Switch `Addresses` to plural fields (`addresses`/`networks`) to match spec semantics; remove singular access and update tests/docs.

### 1.0.4

* Add test for MVR read-write round-trip
* Export matrix only if it carries values
* Export FixtureIDs only if not none

### 1.0.3

* Ensure that layers are created in XML
* Fix header - providerVersion
* Handle empty names
* Make Symdefs to follow XML

### 1.0.2

* Change export XML declaration
* Add missing Source XML export to MappingDefinition
* Remove unused export attributes from Data()

### 1.0.1

* Adjust default class attributes to prevent mutable shared data

### 1.0.0

* Breaking changes, but updating is not complex. There is now an additional
  .scene object, plus several other collector objects. Look at the tests/readme
  for details.
* Big refactor of structure - ensure that XML structure is followed in code
* Implemented all MVR fields
* Big refactor for export

#### 0.5.0

* Add classing to export
* Improve testing of elements availability
* Add python 3.14 beta to testing, add development dependencies
* Add ruff to tests, adjust CI/CD runs

#### Version 0.3.0

- Add MVR writer
- Adjust Fixture - Address
- Convert setup.py to pyproject.toml

#### Version 0.2.0

- Handle faulty XML files with extra null byte
- Handle encoded file names
- Make Geometry3D comparable (Add_more_nodes)
- Reformat with ruff
- Add Capture MVR test file
- Use ruff as a formatter, it's much faster and can configure line length
- AUXData, Data, UserData
- Parse GroupObject as a list
- Add python 3.12 to tests

#### Version 0.1.0

- Initial release
