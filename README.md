# python-mvr

Python library for MVR (My Virtual Rig). MVR is part of [GDTF (General Device Type Format)](https://gdtf-share.com/)

MVR specification as per https://gdtf.eu/mvr/prologue/introduction/

See source code for documentation. Naming conventions, in general, are
identical to that on the GDTF, CamelCase is replaced with
underscore_delimiters.

[Source code](https://github.com/open-stage/python-mvr)

[PyPi page](https://pypi.org/project/pymvr/)

[![Pytest](https://github.com/open-stage/python-mvr/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/open-stage/python-mvr/actions/workflows/run-tests.yaml)

[![Check links in markdown](https://github.com/open-stage/python-mvr/actions/workflows/check-links.yaml/badge.svg)](https://github.com/open-stage/python-mvr/actions/workflows/check-links.yaml)

## Installation

```bash
pip install pymvr
```

To install latest version from git via pip:

```python
python -m pip install https://codeload.github.com/open-stage/python-mvr/zip/refs/heads/master
```

## Usage

### Reading

```python
import pymvr
mvr_scene = pymvr.GeneralSceneDescription("mvr_file.mvr")

for layer_index, layer in enumerate(mvr_scene.layers):
    ... #process data
```

### Writing

```python
fixtures_list = []
mvr = pymvr.GeneralSceneDescriptionWriter()
pymvr.UserData().to_xml(parent=mvr.xml_root)
scene = pymvr.SceneElement().to_xml(parent=mvr.xml_root)
layers = pymvr.LayersElement().to_xml(parent=scene)
layer = pymvr.Layer(name="Test layer").to_xml(parent=layers)
child_list = pymvr.ChildList().to_xml(parent=layer)

fixture = pymvr.Fixture(name="Test Fixture")  # not really a valid fixture
child_list.append(fixture.to_xml())
fixtures_list.append((fixture.gdtf_spec, fixture.gdtf_spec))

pymvr.AUXData().to_xml(parent=scene)

mvr.files_list = list(set(fixtures_list))
mvr.write_mvr("example.mvr")
```

See [BlenderDMX](https://github.com/open-stage/blender-dmx) and
[tests](https://github.com/open-stage/python-mvr/tree/master/tests) for
reference implementation.

## Status

- Reading:

  - Address
  - Alignment
  - AUXData
  - ChildList
  - Class
  - Connection
  - CustomCommand
  - Data
  - Fixture
  - FocusPoint
  - Geometries
  - Geometry3D
  - Gobo
  - GroupObject
  - Layer
  - Mapping
  - Overwrite
  - Position
  - Projector
  - Protocol
  - SceneObject
  - Sources
  - Support
  - Symbol
  - Symdef
  - Truss
  - UserData
  - VideoScreen

- Writing:
  - Fixture
  - Focus point
  - creating MVR zip file

## Development

### Typing

- At this point, the `--no-strict-optional` is needed for mypy tests to pass:

```bash
mypy pymvr/*py  --pretty  --no-strict-optional
```

### Format

- to format, use `ruff`

### Testing

- to test, use `pytest`
- to test typing with mypy use:

```bash
pytest --mypy -m mypy pymvr/*py
```
