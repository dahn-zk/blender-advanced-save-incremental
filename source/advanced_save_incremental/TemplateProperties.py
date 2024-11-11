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

from . import bpyx
from . import core
from .VersionTemplatePropertyGroup import VersionTemplatePropertyGroup

@bpyx.addon_setup.registree
class TemplateProperties(bpy.types.PropertyGroup):
    #
    dirpath_key = "dirpath"
    dirpath_def = bpy.props.StringProperty(
        name = "Directory", default = "//",
        subtype = "DIR_PATH",
        description = (
            "Where to save the files. "
            "Prefix with \"//\" to make the path relative"),
    )
    dirpath: dirpath_def
    #
    prefix_use_key = "prefix_use"
    prefix_use_def = bpy.props.BoolProperty(
        name = "Use Prefix",
        default = True,
        description = "Append a fixed prefix",
    )
    prefix_use: prefix_use_def
    #
    prefix_key = "prefix"
    prefix_def = bpy.props.StringProperty(
        name = "Prefix",
        description = "A fixed prefix",
    )
    prefix: prefix_def
    #
    suffix_use_key = "suffix_use"
    suffix_use_def = bpy.props.BoolProperty(
        name = "Use Suffix",
        default = True,
        description = "Append a fixed suffix",
    )
    suffix_use: suffix_use_def
    #
    suffix_key = "suffix"
    suffix_def = bpy.props.StringProperty(
        name = "Suffix",
        description = "A fixed suffix",
    )
    suffix: suffix_def
    #
    version_use_key = "version_use"
    version_use_def = bpy.props.BoolProperty(
        name = "Use Version",
        default = True,
        description = "Append a numerical version",
    )
    version_use: version_use_def
    #
    version_key = "version"
    version_def = bpy.props.PointerProperty(
        name = "Version",
        type = VersionTemplatePropertyGroup,
        description = "A version template",
    )
    version: version_def
    def version_get(self) -> VersionTemplatePropertyGroup:
        return self.version
    #
    save_copy_key = "save_copy"
    save_copy_def = bpy.props.BoolProperty(
        name = "Copy",
        default = False,
        # description should be the same as in the builtin "Save Copy" operator
        description = (
            "Save a copy of the current working state "
            "and do not make saved file active"),
    )
    save_copy: save_copy_def
    #
    save_overwrite_key = "save_overwrite"
    save_overwrite_def = bpy.props.BoolProperty(
        name = "Overwrite",
        default = False,
        description = "Save and overwrite an existing file without warning",
    )
    save_overwrite: save_overwrite_def
    #
    def core_get(self) -> core.Template:
        return core.Template(
            name = self.name,
            prefix = self.prefix if self.prefix_use else None,
            suffix = self.suffix if self.suffix_use else None,
            version = self.version_get().core_get() if self.version_use else None,
        )
    #
    def to_toml(self) -> str:
        lines = [f'name = "{self.name}"'] if self.name else []
        lines.append(f'{self.dirpath_key} = "{self.dirpath}"')
        if self.prefix_use:
            lines.append(f'{self.prefix_key} = "{self.prefix}"')
        if self.suffix_use:
            lines.append(f'{self.suffix_key} = "{self.suffix}"')
        if self.version_use:
            lines.append(self.version_get().to_toml())
        def bool_str(b: bool):
            return "true" if b else "false"
        lines += [
            f'{self.save_copy_key} = {bool_str(self.save_copy)}',
            f'{self.save_overwrite_key} = {bool_str(self.save_overwrite)}',
        ]
        return '\n'.join(lines)
    #
    def from_dict(self, d: dict):
        if d is not None:
            self.name = d.get("name", self.name)
            if (v := d.get(self.prefix_key)) is not None:
                self.prefix = v
                self.prefix_use = True
            else:
                self.prefix_use = False
            if (v := d.get(self.suffix_key)) is not None:
                self.suffix = v
                self.suffix_use = True
            else:
                self.suffix_use = False
            if (v := d.get(self.version_key)) is not None:
                self.version_get().from_dict(v)
                self.version_use = True
            else:
                self.version_use = False
            if (v := d.get(self.save_copy_key)) is not None:
                self.save_copy = v
            if (v := d.get(self.save_overwrite_key)) is not None:
                self.save_overwrite = v
        return self
