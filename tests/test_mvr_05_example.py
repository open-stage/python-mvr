from pathlib import Path
import pymvr


def test_write_example_mvr_file():
    fixtures_list = []
    mvr = pymvr.GeneralSceneDescriptionWriter()

    layers = pymvr.Layers()
    layer = pymvr.Layer(name="Test layer")
    layers.layers.append(layer)

    child_list = pymvr.ChildList()
    layer.child_list = child_list

    fixture = pymvr.Fixture(name="Test Fixture")  # not really a valid fixture
    child_list.fixtures.append(fixture)
    fixtures_list.append((fixture.gdtf_spec, fixture.gdtf_spec))

    scene = pymvr.Scene(layers=layers)

    scene.to_xml(parent=mvr.xml_root)

    mvr.files_list = list(set(fixtures_list))
    test_file_path = Path(Path(__file__).parent, "example.mvr")
    mvr.write_mvr(test_file_path)
