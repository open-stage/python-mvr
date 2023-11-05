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

```python
import pymvr
mvr_scene = pymvr.GeneralSceneDescription("mvr_file.mvr")

for layer_index, layer in enumerate(mvr_scene.layers):
    ... #process data
```

See [BlenderDMX](https://github.com/open-stage/blender-dmx) and
[tests](https://github.com/open-stage/python-mvr/tree/master/tests) for
reference implementation.

## Status

- Currently implemented:
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

## Development

### Typing

* At this point, the `--no-strict-optional` is needed for mypy tests to pass:

```bash
mypy pymvr/*py  --pretty  --no-strict-optional
```
### Format

- to format, use `ruff`

### Testing

- to test, use `pytest`
- to test typing with mypy use 

```bash
pytest --mypy -m mypy pymvr/*py
```


