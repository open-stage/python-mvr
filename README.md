# python-mvr

Python library for MVR (My Virtual Rig) which is part of [GDTF (General Device Type Format)](https://gdtf-share.com/)

MVR specification as per https://gdtf.eu/mvr/prologue/introduction/

See source code for documentation. Naming conventions, in general, are
identical to that on the GDTF developer wiki, except CamelCase is replaced with
underscore_delimiters.

## Installation

To install from git, run pip:
```python
python -m pip install https://codeload.github.com/open-stage/python-mvr/zip/refs/heads/master
```

## Usage

```python
import pymvr
mvr=pymvr.GeneralSceneDescription("mvr_file.mvr")
```

See [BlenderDMX](https://github.com/open-stage/blender-dmx) and
[tests](https://github.com/open-stage/python-mvr/tree/master/tests) for
reference implementation.

## Status

- This is a very early version, currently implemented:
    - Fixture
    - Layer
    - ChildList
    - GroupObject

## Development

### Typing

* At this point, the `--no-strict-optional` is needed for mypy tests to pass:

```bash
mypy pymvr/*py  --pretty  --no-strict-optional
```
### Format

- to format, use `black`

### Testing

- to test, use `pytest`
- to test typing with mypy use 

```bash
pytest --mypy -m mypy pymvr/*py
```


