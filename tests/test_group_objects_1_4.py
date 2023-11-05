import pytest


@pytest.mark.parametrize("mvr_scene", [("capture_demo_show.mvr",)], indirect=True)
def test_version(mvr_scene):
    """MVR version should be 1.4"""
    assert mvr_scene.version_major == "1"
    assert mvr_scene.version_minor == "4"


@pytest.mark.parametrize("mvr_scene", [("capture_demo_show.mvr",)], indirect=True)
def test_auxdata(mvr_scene):
    """Check symdefs"""
    assert mvr_scene.aux_data.symdefs[0].uuid == "12fcdd5e-4194-56a0-96de-1c3c4edf1cd3"


@pytest.mark.parametrize("mvr_scene", [("capture_demo_show.mvr",)], indirect=True)
def test_child_list(mvr_scene):
    assert mvr_scene.layers[1].child_list.fixtures[0].uuid == "2e149740-6a41-bc43-bd59-8968781b11b9"
    assert mvr_scene.layers[2].child_list.scene_objects[1].uuid == "d1d76649-35bd-9d49-baa4-abcb481fb2c8"
