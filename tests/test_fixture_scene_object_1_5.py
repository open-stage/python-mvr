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
    for layer in mvr_scene.layers:
        process_mvr_child_list(layer.child_list, mvr_scene)

    process_classes(mvr_scene)
