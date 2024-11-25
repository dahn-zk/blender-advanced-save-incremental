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

from pathlib import Path

import bpy

from .. import bpyx

@bpyx.addon_setup.registree
class FilePathProps(bpy.types.PropertyGroup):
    """ property group for UI List Item in the files openers """
    #
    path_key = "path"
    path: bpy.props.StringProperty(name = "Path", subtype = "FILE_PATH")
    def path_get(self) -> str: return self.path
    #
    stem_key = "stem"
    stem: bpy.props.StringProperty(name = "Stem")
    def stem_get(self) -> str: return self.stem
    #
    def set(self, path: Path):
        self.path = str(path)
        self.stem = path.stem
