import pytest
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
    pymvr.UserData().to_xml(parent=mvr.xml_root)
    scene = pymvr.SceneElement().to_xml(parent=mvr.xml_root)
    layers = pymvr.LayersElement().to_xml(parent=scene)
    for layer in data:
        new_layer = pymvr.Layer(name=layer["name"], uuid=layer["uuid"]).to_xml(parent=layers)
        child_list = pymvr.ChildList().to_xml(parent=new_layer)
        for fixture in layer["fixtures"]:
            new_addresses = [
                pymvr.Address(dmx_break=address["dmx_break"], address=address["address"], universe=address["universe"]) for address in fixture["addresses"]
            ]
            new_fixture = pymvr.Fixture(
                name=fixture["gdtf_spec"],
                uuid=fixture["uuid"],
                gdtf_spec=fixture["gdtf_spec"],
                gdtf_mode=fixture["gdtf_mode"],
                fixture_id=fixture["fixture_id"],
                addresses=new_addresses,
            )

            child_list.append(new_fixture.to_xml())
            fixtures_list.append((new_fixture.gdtf_spec, new_fixture.gdtf_spec))

    pymvr.AUXData().to_xml(parent=scene)
    mvr.files_list = list(set(fixtures_list))
    test_file_path = Path(Path(__file__).parent, "test_json.mvr")
    mvr.write_mvr(test_file_path)
