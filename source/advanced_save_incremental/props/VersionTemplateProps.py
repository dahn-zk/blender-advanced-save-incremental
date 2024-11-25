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

from string import digits

import bpy

from .. import bpyx
from .. import core

@bpyx.addon_setup.registree
class VersionTemplateProps(bpy.types.PropertyGroup):
    #
    def _update(self, value):
        # import here to prevent circular dependencies
        from .Props import props_get
        main = props_get()
        if main is None:
            return
        root = main.root_get()
        version_parts = main.version_parts_get()
        for template in main.templates_get():
            if self == template.version_get():
                template.saves_datas_update(root, version_parts)
                break
    #
    separator_key = "separator"
    def separator_set(self, value: str):
        if value and all(d not in value for d in digits):
            self[VersionTemplateProps.separator_key] = value
    def separator_get(self) -> str:
        return self.get(VersionTemplateProps.separator_key, ".")
    separator_def = bpy.props.StringProperty(
        name = "Separator",
        description = "Version elements separator. Cannot be empty or contain digits",
        set = separator_set,
        get = separator_get,
        update = _update,
    )
    separator: separator_def
    #
    count_key = "count"
    count_def = bpy.props.IntProperty(
        name = "Count",
        default = 3,
        min = 1, max = len(core.VersionTemplate.config.parts),
        description = "Version elements count",
        update = _update,
    )
    count: count_def
    def count_get(self) -> int:
        return self.count
    #
    width_key = "width"
    width_def = bpy.props.IntProperty(
        name = "Width",
        default = 1,
        min = 1, max = core.VersionTemplate.config.width_max,
        description = "Version element minimum width",
        update = _update,
    )
    width: width_def
    def width_get(self) -> int:
        return self.width
    #
    def core_get(self) -> core.VersionTemplate:
        return core.VersionTemplate(
            separator = self.separator_get(),
            count = self.count_get(),
            width = self.width_get(),
        )
    #
    def to_toml(self) -> str:
        lines = [f'name = "{self.name}"'] if self.name else []
        lines += [
            f'version.{self.separator_key} = "{self.separator}"',
            f'version.{self.count_key} = {self.count}',
            f'version.{self.width_key} = {self.width}',
        ]
        return '\n'.join(lines)
    #
    def from_dict(self, d: dict):
        if d is not None:
            self.separator = d.get(self.separator_key, self.separator)
            self.count = d.get(self.count_key, self.count)
            self.width = d.get(self.width_key, self.width)
        return self
