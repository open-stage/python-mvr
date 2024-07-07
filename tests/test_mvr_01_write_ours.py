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
            new_fixtures = process_mvr_child_list(
                group.child_list,
                mvr_scene,
            )
            all_fixtures += new_fixtures
            all_focus_points += all_focus_points
    return (all_fixtures, all_focus_points)


@pytest.mark.parametrize("mvr_scene", [("basic_fixture.mvr",)], indirect=True)
def test_write_mvr_file(mvr_scene):
    fixtures_list = []
    mvr = pymvr.GeneralSceneDescriptionWriter()
    pymvr.UserData().to_xml(parent = mvr.xml_root)
    scene = pymvr.SceneElement().to_xml(parent=mvr.xml_root)
    layers = pymvr.LayersElement().to_xml(parent=scene)
    layer = pymvr.Layer(name="My layer").to_xml(parent=layers)
    child_list = pymvr.ChildList().to_xml(parent=layer)
    for layer in mvr_scene.layers:
        fixtures, focus_points = process_mvr_child_list(layer.child_list, mvr_scene)
        for fixture in fixtures:
            child_list.append(fixture.to_xml())
            fixtures_list.append((fixture.gdtf_spec, fixture.gdtf_spec))
        for point in focus_points:
            child_list.append(point.to_xml())

    pymvr.AUXData().to_xml(parent = scene)

    mvr.files_list = list(set(fixtures_list))
    test_file_path = Path(Path(__file__).parent, "test.mvr")
    mvr.write_mvr(test_file_path)
