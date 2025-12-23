# MIT License
#
# Copyright (C) 2023 vanous
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

import shutil
from pathlib import Path
import pytest
import pymvr

# This file sets up a pytest fixtures for the tests
# It is important that this file stays in this location
# as this makes pytest to load pygdtf from the pygdtf directory


@pytest.fixture(scope="function")
def mvr_scene(request, tmp_path):
    def _create_test_mvr(path: Path):
        """Generate a minimal test.mvr matching existing assertions."""
        writer = pymvr.GeneralSceneDescriptionWriter()
        addresses = pymvr.Addresses(
            addresses=[pymvr.Address(dmx_break=1, address=1, universe=1)]
        )
        fixture = pymvr.Fixture(
            name="LED PAR 64 RGBW",
            gdtf_spec="LED PAR 64 RGBW.gdtf",
            gdtf_mode="Default",
            addresses=addresses,
            matrix=pymvr.Matrix(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [5000.0, 5000.0, 5000.0, 0],
                ]
            ),
        )
        layer = pymvr.Layer(
            name="Test layer",
            child_list=pymvr.ChildList(fixtures=[fixture]),
        )
        scene = pymvr.Scene(layers=pymvr.Layers([layer]))
        writer.serialize_scene(scene)
        writer.write_mvr(path)

    def _create_test_json_mvr(path: Path):
        """Generate a minimal test_json.mvr matching existing assertions."""
        writer = pymvr.GeneralSceneDescriptionWriter()
        child_list = pymvr.ChildList()
        fixtures = [
            {
                "gdtf_mode": "Standard mode",
                "uuid": "0153f926-8766-442c-bc5f-57b9407c8e35",
                "addresses": [
                    {"dmx_break": 1, "address": 1, "universe": 1},
                ],
                "gdtf_spec": "BlenderDMX@Basic_LED_Bulb@ver2.gdtf",
                "fixture_id": 1,
            },
            {
                "gdtf_mode": "Standard mode",
                "uuid": "5321f77d-4647-48b6-8798-25ac9292cc2d",
                "addresses": [
                    {"dmx_break": 1, "address": 10, "universe": 1},
                ],
                "gdtf_spec": "BlenderDMX@Basic_LED_Bulb@ver2.gdtf",
                "fixture_id": 1,
            },
        ]

        for fixture_data in fixtures:
            new_addresses = [
                pymvr.Address(
                    dmx_break=address["dmx_break"],
                    address=address["address"],
                    universe=address["universe"],
                )
                for address in fixture_data["addresses"]
            ]

            child_list.fixtures.append(
                pymvr.Fixture(
                    name=fixture_data["gdtf_spec"],
                    uuid=fixture_data["uuid"],
                    gdtf_spec=fixture_data["gdtf_spec"],
                    gdtf_mode=fixture_data["gdtf_mode"],
                    fixture_id=fixture_data["fixture_id"],
                    addresses=pymvr.Addresses(addresses=new_addresses),
                    matrix=pymvr.Matrix(0),
                )
            )

        layer = pymvr.Layer(
            name="Layer 1",
            uuid="1e4954b5-992c-4146-b71f-5b497834087f",
            child_list=child_list,
        )
        scene = pymvr.Scene(layers=pymvr.Layers([layer]))
        writer.serialize_scene(scene)
        writer.write_mvr(path)

    file_name = request.param[0]
    test_mvr_scene_path = Path(
        Path(__file__).parents[0], "tests", file_name
    )  # test file path is made from current directory, tests directory and a file name
    generated_path = tmp_path / file_name
    if test_mvr_scene_path.is_file():
        shutil.copy(test_mvr_scene_path, generated_path)
    elif file_name == "test.mvr":
        _create_test_mvr(generated_path)
    elif file_name == "test_json.mvr":
        _create_test_json_mvr(generated_path)
    else:
        pytest.skip(f"Test file {file_name} is not available")

    mvr_scene = pymvr.GeneralSceneDescription(generated_path)
    yield mvr_scene


@pytest.fixture(scope="function")
def pymvr_module():
    yield pymvr


def pytest_configure(config):
    plugin = config.pluginmanager.getplugin("mypy")
    # plugin.mypy_argv.append("--no-strict-optional")


def pytest_addoption(parser):
    parser.addoption(
        "--file-path", action="store", default=None, help="Path to the input file"
    )
