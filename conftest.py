from pathlib import Path
import pytest
import pymvr

# This file sets up a pytest fixtures for the tests
# It is important that this file stays in this location
# as this makes pytest to load pygdtf from the pygdtf directory


@pytest.fixture(scope="function")
def mvr_scene(request):
    file_name = request.param[0]
    test_mvr_scene_path = Path(
        Path(__file__).parents[0], "tests", file_name
    )  # test file path is made from current directory, tests directory and a file name
    mvr_scene = pymvr.GeneralSceneDescription(test_mvr_scene_path)
    yield mvr_scene


@pytest.fixture(scope="session")
def pymvr_module():
    yield pymvr


def pytest_configure(config):
    plugin = config.pluginmanager.getplugin("mypy")
    plugin.mypy_argv.append("--no-strict-optional")
