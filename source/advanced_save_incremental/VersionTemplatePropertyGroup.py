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

import string

import bpy

from . import bpyx
from . import core

@bpyx.addon_setup.registree
class VersionTemplatePropertyGroup(bpy.types.PropertyGroup):
    #
    separator_key = "separator"
    def separator_set(self, value: str):
        if value and all(d not in value for d in string.digits):
            self[VersionTemplatePropertyGroup.separator_key] = value
    def separator_get(self) -> str:
        return self.get(VersionTemplatePropertyGroup.separator_key, ".")
    separator_def = bpy.props.StringProperty(
        name = "Separator",
        description = (
            "Version elements separator. Cannot be empty or contain digits"),
        set = separator_set,
        get = separator_get,
    )
    separator: separator_def
    #
    count_key = "count"
    count_def = bpy.props.IntProperty(
        name = "Count",
        default = 3,
        min = 1, max = len(core.VersionTemplate.config.parts),
        description = "Version elements count",
    )
    count: count_def
    #
    width_key = "width"
    width_def = bpy.props.IntProperty(
        name = "Width",
        default = 1,
        min = 1, max = core.VersionTemplate.config.width_max,
        description = "Version element minimum width",
    )
    width: width_def
    ###
    def core_get(self) -> core.VersionTemplate:
        return core.VersionTemplate(
            separator = self.separator,
            count = self.count,
            width = self.width,
        )
