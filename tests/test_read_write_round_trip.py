# MIT License
#
# Copyright (C) 2025 vanous
#
# This file is part of pymvr.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest
import os
from pathlib import Path


def test_read_write_round_trip(request, pymvr_module):
    # tests a single file, reading and then exporting
    # does not pack resources, only the XML
    # uv run pytest --file-path=/path/to/file.mvr -s -x
    file_path = request.config.getoption("--file-path")

    if file_path is None:
        pytest.skip("File path not provided")
    file_read_path = Path(file_path)
    if not file_read_path.is_file():
        pytest.skip("File does not exist")
    file_read_dir = file_read_path.parent
    file_read_name = file_read_path.stem
    file_write_path = Path(file_read_dir, f"{file_read_name}_exported.mvr")

    with pymvr_module.GeneralSceneDescription(file_read_path) as mvr_read:
        mvr_writer = pymvr_module.GeneralSceneDescriptionWriter()

        mvr_read.scene.to_xml(parent=mvr_writer.xml_root)
        mvr_read.user_data.to_xml(parent=mvr_writer.xml_root)

        mvr_writer.write_mvr(file_write_path)
