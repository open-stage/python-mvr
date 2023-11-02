import pytest


@pytest.mark.parametrize("mvr_scene", [("basic_fixture.mvr",)], indirect=True)
def test_version(mvr_scene):
    """MVR version should be 1.5"""

    assert mvr_scene.version_major == "1"
    assert mvr_scene.version_minor == "5"


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
    assert fixture.addresses[0].universe == 1
    assert fixture.addresses[0].address == 0
    assert fixture.gdtf_mode == "Default"
    assert fixture.matrix.matrix[3] == [5.0, 5.0, 5.0, 0]


@pytest.mark.parametrize("mvr_scene", [("basic_fixture.mvr",)], indirect=True)
def test_fixture(mvr_scene):
    for layer in mvr_scene.layers:
        process_mvr_child_list(layer.child_list, mvr_scene)
