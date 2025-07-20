import pymvr


def test_write_example_mvr_file():
    fixtures_list = []
    mvr = pymvr.GeneralSceneDescriptionWriter()
    pymvr.UserData().to_xml(parent=mvr.xml_root)
    scene = pymvr.SceneElement().to_xml(parent=mvr.xml_root)
    layers = pymvr.LayersElement().to_xml(parent=scene)
    layer = pymvr.Layer(name="Test layer").to_xml(parent=layers)
    child_list = pymvr.ChildList().to_xml(parent=layer)

    fixture = pymvr.Fixture(name="Test Fixture")  # not really a valid fixture
    child_list.append(fixture.to_xml())
    fixtures_list.append((fixture.gdtf_spec, fixture.gdtf_spec))

    pymvr.AUXData().to_xml(parent=scene)

    mvr.files_list = list(set(fixtures_list))
    mvr.write_mvr("example.mvr")
