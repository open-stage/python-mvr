# python-mvr

Python library for MVR (My Virtual Rig). MVR is part of [GDTF (General Device Type Format)](https://gdtf-share.com/)

MVR specification as per https://gdtf.eu/mvr/prologue/introduction/

See source code for documentation. Naming conventions, in general, are
identical to that on the GDTF, CamelCase is replaced with
underscore\_delimiters.

This library is used for example by [BlenderDMX](https://blenderdmx.eu)
([BlenderDMX on GitHub](https://github.com/open-stage/blender-dmx)).

[GitHub Page](https://github.com/open-stage/python-mvr), [PyPi Page](https://pypi.org/project/pymvr/)

[![Pytest](https://github.com/open-stage/python-mvr/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/open-stage/python-mvr/actions/workflows/run-tests.yaml)
[![Check links in markdown](https://github.com/open-stage/python-mvr/actions/workflows/check-links.yaml/badge.svg)](https://github.com/open-stage/python-mvr/actions/workflows/check-links.yaml)
![GitHub Tag](https://img.shields.io/github/v/tag/open-stage/python-mvr)

## Status

- Reading and Writing of most aspects of MVR should be covered.

## Installation

- With uv:

```bash
uv add pymvr
```

- With pip

```bash
pip install pymvr
```

### Latest development version (if exists on pypi.org)

```bash
uv add pymvr --pre
```

## Usage

### Reading MVR

```python
import pymvr
mvr_file = pymvr.GeneralSceneDescription("mvr_file.mvr")

for layer_index, layer in enumerate(mvr_file.scene.layers):
    ... #process data
```

### Writing MVR

#### Creating a new MVR

```python
import pymvr
from pathlib import Path

# 1. Create a writer instance
mvr_writer = pymvr.GeneralSceneDescriptionWriter()

# 2. Build the MVR object tree
# Create a scene object
scene_obj = pymvr.Scene()

# Create layers and add them to the scene
layers = pymvr.Layers()
scene_obj.layers = layers

# Create a layer and add it to the layers
layer = pymvr.Layer(name="Test layer")
layers.append(layer)

# Create a child list for the layer
child_list = pymvr.ChildList()
layer.child_list = child_list

# Create a fixture and add it to the child list
# Note: A valid fixture would require more attributes
fixture = pymvr.Fixture(name="Test Fixture")
child_list.fixtures.append(fixture)

# 3. Serialize the scene object into the writer's XML root
scene_obj.to_xml(parent=mvr_writer.xml_root)

# 4. Add any necessary files (like GDTF) to the MVR archive
# (This example fixture doesn't have a GDTF file, so this list will be empty)
files_to_pack = []
if fixture.gdtf_spec:
    # The list should contain tuples of (source_path, archive_name)
    files_to_pack.append((fixture.gdtf_spec, fixture.gdtf_spec))
mvr_writer.files_list = list(set(files_to_pack))

# 5. Write the MVR file
output_path = Path("example.mvr")
mvr_writer.write_mvr(output_path)

print(f"MVR file written to {output_path.resolve()}")
```

#### Exporting loaded MVR

```python
import pymvr
from pathlib import Path


# 1. Read MVR file
mvr_read = pymvr.GeneralSceneDescription("mvr_file.mvr")

# 2. Create a writer instance
mvr_writer = pymvr.GeneralSceneDescriptionWriter()

# 3. Serialize the scene object into the writer's XML root
mvr_read.scene.to_xml(parent=mvr_writer.xml_root)

# 4. Add necesarry files if needed
# Skipped in this example

# 5. Write the MVR file
output_path = Path("example.mvr")
mvr_writer.write_mvr(output_path)

print(f"MVR file written to {output_path.resolve()}")
```

See [BlenderDMX](https://github.com/open-stage/blender-dmx) and
[tests](https://github.com/open-stage/python-mvr/tree/master/tests) for
reference implementation.

## Development

PRs appreciated. You can use [uv](https://docs.astral.sh/uv/) to get the
project setup by running:

```bash
uv sync
```

### Format

- To format, use [ruff](https://docs.astral.sh/ruff/)

```bash
uv run ruff format pymvr/*
```

### Pre-commit hooks

- You can use the pre-commit hooks

```bash
uv run pre-commit install
```

### Testing

- To test, use pytest

```bash
uv run pytest
```

- To test typing with mypy use:

```bash
uv run pytest --mypy -m mypy pymvr/*py
```
