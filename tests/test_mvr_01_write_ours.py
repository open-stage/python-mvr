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
