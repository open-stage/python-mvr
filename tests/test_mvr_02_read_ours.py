# MIT License
#
# Copyright (C) 2024 vanous
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

import pytest


@pytest.mark.parametrize("mvr_scene", [("test.mvr",)], indirect=True)
def test_version(mvr_scene):
    """MVR version should be 1.6"""

    assert mvr_scene.version_major == "1"
    assert mvr_scene.version_minor == "6"


def process_mvr_child_list(child_list, mvr_scene):
    for fixture in child_list.fixtures:
        process_mvr_fixture(fixture)
    for group in child_list.group_objects:
        if group.child_list is not None:
            process_mvr_child_list(
                group.child_list,
                mvr_scene,
            )


def process_mvr_fixture(fixture):
    assert fixture.gdtf_spec == "LED PAR 64 RGBW.gdtf"
    assert fixture.addresses.addresses[0].universe == 1
    assert fixture.addresses.addresses[0].address == 1
    assert fixture.gdtf_mode == "Default"
    assert fixture.matrix.matrix[3] == [5000.0, 5000.0, 5000.0, 0]


@pytest.mark.parametrize("mvr_scene", [("test.mvr",)], indirect=True)
def test_fixture(mvr_scene):
    assert len(mvr_scene.scene.layers) > 0
    for layer in mvr_scene.scene.layers:
        process_mvr_child_list(layer.child_list, mvr_scene)
