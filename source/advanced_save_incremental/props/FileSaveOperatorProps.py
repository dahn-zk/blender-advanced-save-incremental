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

import bpy

from .. import bpyx
from ..core import FileSaveData

@bpyx.addon_setup.registree
class FileSaveOperatorProps(bpy.types.PropertyGroup):
    #
    filename_key = "filename"
    filename_def = bpy.props.StringProperty(
        name = "File Name",
        description = "File name to save (computed value)",
    )
    filename: filename_def
    def file_name_set(self, v: str):
        self.filename = v
    def file_name_get(self) -> str:
        return self.filename
    #
    label_key = "label"
    label_def = bpy.props.StringProperty(
        name = "Label",
        description = "Button label",
    )
    label: label_def
    def label_set(self, v: str):
        self.label = v
    def label_get(self) -> str:
        return self.label
    #
    def from_core(self, v: FileSaveData):
        self.file_name_set(v.file_name)
        self.label_set(v.label)
