# MIT License
#
# Copyright (C) 2025 vanous
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

from pathlib import Path
import pymvr


def test_write_from_json():
    # TODO: add some assertions
    data = [
        {
            "name": "Layer 1",
            "uuid": "1e4954b5-992c-4146-b71f-5b497834087f",
            "fixtures": [
                {
                    "gdtf_mode": "Standard mode",
                    "uuid": "0153f926-8766-442c-bc5f-57b9407c8e35",
                    "addresses": [{"dmx_break": 1, "address": 1, "universe": 1}],
                    "gdtf_spec": "BlenderDMX@Basic_LED_Bulb@ver2.gdtf",
                    "fixture_id": 1,
                },
                {
                    "gdtf_mode": "Standard mode",
                    "uuid": "5321f77d-4647-48b6-8798-25ac9292cc2d",
                    "addresses": [{"dmx_break": 1, "address": 10, "universe": 1}],
                    "gdtf_spec": "BlenderDMX@Basic_LED_Bulb@ver2.gdtf",
                    "fixture_id": 1,
                },
            ],
        }
    ]
    fixtures_list = []
    mvr = pymvr.GeneralSceneDescriptionWriter()
    layers = pymvr.Layers()
    for layer_data in data:
        layer = pymvr.Layer(name=layer_data["name"], uuid=layer_data["uuid"])
        layers.append(layer)
        child_list = pymvr.ChildList()
        layer.child_list = child_list

        for fixture_data in layer_data["fixtures"]:
            new_addresses = [
                pymvr.Address(
                    dmx_break=address["dmx_break"],
                    address=address["address"],
                    universe=address["universe"],
                )
                for address in fixture_data["addresses"]
            ]

            new_fixture = pymvr.Fixture(
                name=fixture_data["gdtf_spec"],
                uuid=fixture_data["uuid"],
                gdtf_spec=fixture_data["gdtf_spec"],
                gdtf_mode=fixture_data["gdtf_mode"],
                fixture_id=fixture_data["fixture_id"],
                addresses=pymvr.Addresses(address=new_addresses),
            )

            child_list.fixtures.append(new_fixture)
            fixtures_list.append((new_fixture.gdtf_spec, new_fixture.gdtf_spec))

    scene = pymvr.Scene(layers=layers)
    scene.to_xml(mvr.xml_root)
    test_file_path = Path(Path(__file__).parent, "test_json.mvr")
    mvr.write_mvr(test_file_path)
