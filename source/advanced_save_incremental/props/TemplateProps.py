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
from .. import core
from ..prefs.Preferences import Preferences
from .FilePathProps import FilePathProps
from .FileSaveOperatorProps import FileSaveOperatorProps
from .VersionTemplateProps import VersionTemplateProps

@bpyx.addon_setup.registree
class TemplateProps(bpy.types.PropertyGroup):
    #
    def save_datas_update(self, value = None):
        if type(self) != TemplateProps:
            return
        # import here to prevent circular dependencies
        from .Props import props_get
        main = props_get()
        if main is None:
            return
        root = main.root_get()
        version_parts = main.version_parts_get()
        self.saves_datas_update(root, version_parts)
    #
    dirpath_key = "dirpath"
    dirpath_def = bpy.props.StringProperty(
        name = "Directory", default = "//",
        subtype = 'DIR_PATH',
        description = "Where to save the files. Prefix with \"//\" to make the path relative",
        update = save_datas_update,
    )
    dirpath: dirpath_def
    #
    prefix_use_key = "prefix_use"
    prefix_use_def = bpy.props.BoolProperty(
        name = "Use Prefix",
        default = True,
        description = "Append a fixed prefix",
        update = save_datas_update,
    )
    prefix_use: prefix_use_def
    #
    prefix_key = "prefix"
    prefix_def = bpy.props.StringProperty(
        name = "Prefix",
        description = "A fixed prefix",
        update = save_datas_update,
    )
    prefix: prefix_def
    #
    suffix_use_key = "suffix_use"
    suffix_use_def = bpy.props.BoolProperty(
        name = "Use Suffix",
        default = True,
        description = "Append a fixed suffix",
        update = save_datas_update,
    )
    suffix_use: suffix_use_def
    #
    suffix_key = "suffix"
    suffix_def = bpy.props.StringProperty(
        name = "Suffix",
        description = "A fixed suffix",
        update = save_datas_update,
    )
    suffix: suffix_def
    #
    version_use_key = "version_use"
    version_use_def = bpy.props.BoolProperty(
        name = "Use Version",
        default = True,
        description = "Append a numerical version",
        update = save_datas_update,
    )
    version_use: version_use_def
    #
    version_key = "version"
    version_def = bpy.props.PointerProperty(
        name = "Version",
        type = VersionTemplateProps,
        description = "A version template",
        update = save_datas_update,
    )
    version: version_def
    def version_get(self) -> VersionTemplateProps:
        return self.version
    #
    save_copy_key = "save_copy"
    save_copy_def = bpy.props.BoolProperty(
        name = "Copy",
        default = False,
        # description should be the same as in the builtin "Save Copy" operator
        description = "Save a copy of the current working state and do not make saved file active",
        update = save_datas_update,
    )
    save_copy: save_copy_def
    def save_copy_get(self) -> bool:
        return self.save_copy
    #
    save_overwrite_key = "save_overwrite"
    save_overwrite_def = bpy.props.BoolProperty(
        name = "Overwrite",
        default = False,
        description = "Save and overwrite an existing file without warning",
        update = save_datas_update,
    )
    save_overwrite: save_overwrite_def
    def save_overwrite_get(self) -> bool:
        return self.save_overwrite
    #
    def core_get(self) -> core.Template:
        return core.Template(
            name = self.name,
            prefix = self.prefix if self.prefix_use else None,
            suffix = self.suffix if self.suffix_use else None,
            version = self.version_get().core_get() if self.version_use else None,
        )
    #
    # computed save buttons data
    saves_datas_key = "saves_datas"
    saves_datas_def = bpy.props.CollectionProperty(
        name = "Save Operators Data",
        description = "Data for save operators",
        type = FileSaveOperatorProps,
    )
    saves_data: saves_datas_def
    def saves_datas_get(self) -> bpyx.PropCollection[FileSaveOperatorProps]:
        return self.saves_data
    def saves_datas_update(self, root: str, version_parts: core.VersionParts):
        datas = self.saves_datas_get()
        datas.clear()
        phrase = (("Overwrite" if self.save_overwrite_get() else "Save") +
                  (" Copy" if self.save_copy_get() else ""))
        for core_save_data in core.build.files_save_datas_gen(
                template = self.core_get(),
                version_parts = version_parts,
                root = root, phrase = phrase):
            datas.add().from_core(core_save_data)
    #
    # files openers
    files_key = "files"
    files: bpy.props.CollectionProperty(
        name = "Files",
        type = FilePathProps,
    )
    def files_get(self) -> bpyx.PropCollection[FilePathProps]:
        return self.files
    #
    # required by the UI API
    files_active_index_key = "files_active_index"
    files_active_index: bpy.props.IntProperty(
        name = "Active File Index",
    )
    #
    ui_opened_key = "ui_opened"
    ui_opened: bpy.props.BoolProperty(
        name = "Open Template",
        default = True,
    )
    #
    ui_show_files_key = "ui_show_files"
    ui_show_files: bpy.props.BoolProperty(
        name = "Show Files",
        default = False,
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
    #
    def files_update(self, root: str):
        directory_path = bpyx.path_abs_get(self.dirpath)
        if directory_path.exists():
            self.files_get().clear()
        should_load_all = Preferences.instance_get().should_load_all_files_get()
        if not should_load_all and root:
            pattern = f"*{root}*.blend"
        else:
            pattern = "*.blend"
        other_files_paths = list(directory_path.glob(pattern))
        for other_file_path in other_files_paths:
            self.files_get().add().set(other_file_path)
    #
    def update(self, root: str, version_parts: core.VersionParts):
        self.saves_datas_update(root, version_parts)
        self.files_update(root)
