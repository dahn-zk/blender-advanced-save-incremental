# Copyright (C) 2024 Danylo Dubinin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
miscellaneous reusable Blender code not depending on a specific addon
"""

from pathlib import Path
from typing import TypeVar

import bpy

bl_path_str = TypeVar("bl_path_str", bound = str)
""" to denote Blender-style strings denoting paths """

def path_abs_get(path: bl_path_str) -> Path:
    return Path(bpy.path.abspath(path))

def file_path_get() -> Path:
    return path_abs_get(bpy.data.filepath)
