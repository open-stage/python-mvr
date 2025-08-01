### Changelog

### 1.0.0-dev0

* Breaking changes. There is now an additional .scene object, plus several
  other collector objects. Look at the tests/readme for details.
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
