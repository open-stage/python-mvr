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


@pytest.mark.parametrize("mvr_scene", [("scene_objects.mvr",)], indirect=True)
def test_version(mvr_scene):
    """MVR version should be 1.5"""

    assert mvr_scene.version_major == "1"
    assert mvr_scene.version_minor == "5"


def process_mvr_child_list(child_list, mvr_scene):
    for fixture in child_list.fixtures:
        process_mvr_fixture(fixture)

    for focus_point in child_list.focus_points:
        process_mvr_focus_point(focus_point)

    for scene_object in child_list.scene_objects:
        process_mvr_scene_object(scene_object)

    for group in child_list.group_objects:
        if group.child_list is not None:
            process_mvr_child_list(
                group.child_list,
                mvr_scene,
            )


def process_mvr_fixture(fixture):
    assert fixture.gdtf_spec == "Custom@Light Instr Light Source Pendant 44deg.gdtf"
    assert fixture.gdtf_mode == "DMX Mode"


def process_mvr_scene_object(scene_object):
    # test getting focus points
    name = scene_object.name
    uuid = scene_object.uuid
    assert name is not None
    assert uuid is not None
    print("scene object", name, uuid)


def process_mvr_focus_point(focus_point):
    # test getting focus points
    name = focus_point.name
    uuid = focus_point.uuid
    assert name is not None
    assert uuid is not None
    print("focus point", name, uuid)


def process_classes(mvr_scene):
    class_ = mvr_scene.aux_data.classes[0]
    assert class_.name == "Site-Cieling"
    assert class_.uuid == "2BD0B4C7-DDE3-4CAE-AA8D-9DDDF096F43E"


@pytest.mark.parametrize("mvr_scene", [("scene_objects.mvr",)], indirect=True)
def test_fixture(mvr_scene):
    for layer in mvr_scene.scene.layers:
        process_mvr_child_list(layer.child_list, mvr_scene)

    process_classes(mvr_scene.scene)
