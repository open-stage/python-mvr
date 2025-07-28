# The MIT License (MIT)
#
# Copyright (C) 2023 vanous
#
# This file is part of pymvr.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the “Software”), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest


@pytest.mark.parametrize("mvr_scene", [("capture_demo_show.mvr",)], indirect=True)
def test_version(mvr_scene):
    """MVR version should be 1.4"""
    assert mvr_scene.version_major == "1"
    assert mvr_scene.version_minor == "4"


@pytest.mark.parametrize("mvr_scene", [("capture_demo_show.mvr",)], indirect=True)
def test_auxdata(mvr_scene):
    """Check symdefs"""
    assert (
        mvr_scene.scene.aux_data.symdefs[0].uuid
        == "12fcdd5e-4194-56a0-96de-1c3c4edf1cd3"
    )


@pytest.mark.parametrize("mvr_scene", [("capture_demo_show.mvr",)], indirect=True)
def test_child_list(mvr_scene):
    assert (
        mvr_scene.scene.layers[1].child_list.fixtures[0].uuid
        == "2e149740-6a41-bc43-bd59-8968781b11b9"
    )
    assert (
        mvr_scene.scene.layers[2].child_list.scene_objects[1].uuid
        == "d1d76649-35bd-9d49-baa4-abcb481fb2c8"
    )
