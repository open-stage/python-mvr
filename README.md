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
mvr_file = pymvr.GeneralSceneDescription("mvr_file.mvr")

for layer_index, layer in enumerate(mvr_file.scene.layers):
    ... #process data
```

### Writing

```python

mvr = pymvr.GeneralSceneDescriptionWriter()
pymvr.UserData().to_xml(parent=mvr.xml_root)
scene = pymvr.Scene().to_xml(parent=mvr.xml_root)
pymvr.AUXData().to_xml(parent=scene)
fixtures_list = []

layers = pymvr.Layers()
layer = pymvr.Layer(name="Test layer")
layers.layers.append(layer)

child_list = pymvr.ChildList()
layer.child_list = child_list

fixture = pymvr.Fixture(name="Test Fixture")  # not really a valid fixture
child_list.fixtures.append(fixture)
fixtures_list.append((fixture.gdtf_spec, fixture.gdtf_spec))

layers.to_xml(parent=scene)

mvr.files_list = list(set(fixtures_list))
test_file_path = Path(Path(__file__).parent, "example.mvr")
mvr.write_mvr(test_file_path)
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

PRs appreciated. You can use [uv](https://docs.astral.sh/uv/) to get the
project setup by running:

```bash
uv sync
```

### Typing

- We try to type the main library, at this point, the
  `--no-strict-optional` is needed for mypy tests to pass:

```bash
mypy pymvr/*py  --pretty  --no-strict-optional
```

### Format

- To format, use [black](https://github.com/psf/black) or
  [ruff](https://docs.astral.sh/ruff/)

### Testing

- to test, use pytest

```bash
pytest
```

- to test typing with mypy use:

```bash
pytest --mypy -m mypy pymvr/*py
```
