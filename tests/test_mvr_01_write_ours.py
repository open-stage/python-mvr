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
from pathlib import Path
import pymvr


def process_mvr_child_list(child_list, mvr_scene):
    all_fixtures = []
    all_focus_points = []

    all_fixtures += child_list.fixtures
    all_focus_points += child_list.focus_points

    for group in child_list.group_objects:
        if group.child_list is not None:
            new_fixtures, new_focus_points = process_mvr_child_list(
                group.child_list,
                mvr_scene,
            )
            all_fixtures += new_fixtures
            all_focus_points += new_focus_points
    return (all_fixtures, all_focus_points)


@pytest.mark.parametrize("mvr_scene", [("basic_fixture.mvr",)], indirect=True)
def test_write_mvr_file(mvr_scene):
    mvr = pymvr.GeneralSceneDescriptionWriter()
    mvr_scene.scene.to_xml(mvr.xml_root)
    mvr_scene.user_data.to_xml(mvr.xml_root)
    # TODO: add back file iteration to include gdtf files in the zip file

    test_file_path = Path(Path(__file__).parent, "test.mvr")
    mvr.write_mvr(test_file_path)
