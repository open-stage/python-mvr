import pytest


@pytest.mark.parametrize("mvr_scene", [("test_json.mvr",)], indirect=True)
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
    assert fixture.gdtf_spec == "BlenderDMX@Basic_LED_Bulb@ver2.gdtf"
    assert fixture.addresses[0].dmx_break == 1
    assert fixture.addresses[0].universe == 1
    assert fixture.gdtf_mode == "Standard mode"
    assert fixture.matrix.matrix[3] == [0.0, 0.0, 0.0, 0]


@pytest.mark.parametrize("mvr_scene", [("test_json.mvr",)], indirect=True)
def test_fixture(mvr_scene):
    for layer in mvr_scene.layers:
        assert layer.name == "Layer 1"
        assert layer.uuid == "1e4954b5-992c-4146-b71f-5b497834087f"
        process_mvr_child_list(layer.child_list, mvr_scene)
