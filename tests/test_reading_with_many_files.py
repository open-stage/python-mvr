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


def test_reading_with_many_files(request, pymvr_module):
    # uv run pytest --file-path=../../gdtfs/ -s
    file_path = request.config.getoption("--file-path")

    if file_path is None:
        pytest.skip("File path not provided")

    path = Path(file_path)
    files = list(path.glob("*.mvr"))
    sorted_files = sorted(files, key=os.path.getmtime, reverse=True)

    if not sorted_files:
        pytest.skip(f"No files found in {file_path} matching the pattern")

    for file in sorted_files:
        print(file)
        with pymvr_module.GeneralSceneDescription(file) as f:
            print(f.version_major, f.version_minor, f.provider, f.provider_version)
