# The MIT License (MIT)
#
# Copyright (C) 2023 vanous
#
# This file is part of pymvr.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the “Software”), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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


@pytest.fixture(scope="function")
def pymvr_module():
    yield pymvr


def pytest_configure(config):
    plugin = config.pluginmanager.getplugin("mypy")
    # plugin.mypy_argv.append("--no-strict-optional")


def pytest_addoption(parser):
    parser.addoption(
        "--file-path", action="store", default=None, help="Path to the input file"
    )
