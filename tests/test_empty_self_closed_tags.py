# MIT License
#
# Copyright (C) 2026 vanous
#
# This file is part of pymvr.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import zipfile

import pytest
import pymvr


@pytest.mark.parametrize("mvr_scene", [("empty-tags.mvr",)], indirect=True)
def test_empty_self_closed_tags_parse(mvr_scene):
    layer = mvr_scene.scene.layers[0]
    fixture = layer.child_list.fixtures[0]

    assert len(fixture.addresses) == 0
    assert len(fixture.protocols) == 0
    assert len(fixture.mappings) == 0
    assert len(fixture.alignments) == 0
    assert len(fixture.custom_commands) == 0
    assert len(fixture.overwrites) == 0
    assert len(fixture.connections) == 0


@pytest.mark.parametrize("mvr_scene", [("empty-tags.mvr",)], indirect=True)
def test_empty_self_closed_tags_write_omits(mvr_scene, tmp_path):
    mvr = pymvr.GeneralSceneDescriptionWriter()
    mvr_scene.scene.to_xml(mvr.xml_root)

    test_file_path = tmp_path / "test-empty-tags.mvr"
    mvr.write_mvr(test_file_path)

    with zipfile.ZipFile(test_file_path, "r") as archive:
        data = archive.read("GeneralSceneDescription.xml")

    assert b"<Addresses" not in data
    assert b"<Protocols" not in data
    assert b"<Mappings" not in data
    assert b"<Alignments" not in data
    assert b"<CustomCommands" not in data
    assert b"<Overwrites" not in data
    assert b"<Connections" not in data
    assert b"<Sources" not in data
    assert b"<Projections" not in data
