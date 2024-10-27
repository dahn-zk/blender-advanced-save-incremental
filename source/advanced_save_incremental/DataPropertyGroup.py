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

import logging
import textwrap
from pathlib import Path

import bpy

from . import bpyx
from . import config
from . import core
from .FilePathProperties import FilePathProperties
from .Globals import Globals
from .Preferences import Preferences
from .StoredTemplateProperties import StoredTemplateProperties
from .TemplateProperties import TemplateProperties

logger = logging.getLogger(__name__)

@bpyx.addon_setup.registree
@bpyx.addon_setup.custom_property_pointer(bpy.types.Text, Globals.data_key)
class DataPropertyGroup(bpy.types.PropertyGroup):
    """ what is stored in a blend-file """
    def _update(self, value):
        data_parse(self)
    #
    ### input properties
    prefix_key = "prefix"
    prefix_def = bpy.props.StringProperty(
        name = "Prefix",
        description = "Current file prefix if any",
        update = _update,
    )
    prefix: prefix_def
    #
    suffix_key = "suffix"
    suffix_def = bpy.props.StringProperty(
        name = "Suffix",
        description = "Current file suffix if any",
        update = _update,
    )
    suffix: suffix_def
    #
    version_separator_key = "version_separator"
    def version_separator_set(self, value):
        if value: self[DataPropertyGroup.version_separator_key] = value
    def version_separator_get(self) -> str:
        return self.get(DataPropertyGroup.version_separator_key, ".")
    version_separator_def = bpy.props.StringProperty(
        name = "Version Separator",
        description = "Version elements separator. Cannot be empty",
        set = version_separator_set,
        get = version_separator_get,
        update = _update,
    )
    version_separator: version_separator_def
    #
    version_count_key = "version_count"
    version_count_def = bpy.props.IntProperty(
        name = "Version Count",
        default = 3,
        min = 1,
        max = len(core.VersionTemplate.config.parts),
        description = "Version elements count",
        update = _update,
    )
    version_count: version_count_def
    #
    def version_template_get(self): return core.VersionTemplate(
        separator = self.version_separator,
        count = self.version_count,
        width = 0,
    )
    #
    ### computed properties
    root_key = "root"
    root_def = bpy.props.StringProperty(
        name = "Name Root",
        options = {'HIDDEN'},
        description = "Name part without version and affixes. Meant to be read-only",
    )
    root: root_def
    #
    version_value_key = "version_value"
    version_value_def = bpy.props.StringProperty(
        name = "Version",
        options = {'HIDDEN'},
        description = "Name part containing only version. Meant to be read-only",
    )
    version_value: version_value_def
    def version_value_get(self) -> str:
        return self.version_value
    #
    ### other properties and UI state
    def version_parts_get(self):
        version_parts = self.version_value_get().split(
            self.version_template_get().separator)
        return [int(e) for e in version_parts if e.isnumeric()]
    #
    def template_core_get(self):
        return core.Template(self.prefix, self.suffix, self.version_template_get())
    #
    templates_key = "templates"
    templates_def = bpy.props.CollectionProperty(
        name = "Files",
        type = StoredTemplateProperties,
    )
    templates: templates_def
    def templates_get(self) -> bpyx.PropCollection[StoredTemplateProperties]:
        return self.templates
    #
    ui_show_template_key = "ui_show_template"
    ui_show_template_def = bpy.props.BoolProperty(
        name = "Show Template",
        default = True,
    )
    ui_show_template: ui_show_template_def
    #
    ui_list_buttons_key = "ui_list_buttons"
    ui_list_buttons_def = bpy.props.BoolProperty(
        name = "Show List Operators",
        default = True,
    )
    ui_list_buttons: ui_list_buttons_def
    #
def data_get(text_name: str) -> DataPropertyGroup:
    text = bpy.data.texts.get(text_name)
    return getattr(text, Globals.data_key) if text is not None else None
def info_code_get(data):
    comment = textwrap.indent(textwrap.fill(
        f"This Text stores {Globals.addon_qname} add-on data in hidden "
        f"custom properties. It can be safely deleted if you do not use "
        f"this add-on in this Blender file."
        f"The code below is just informational for ease of debugging/hacking "
        f"if you need to."), "# ")
    code = "\n".join(
        [
            "",
            f"import {__package__} as asi",
            "",
            "# data",
            repr(data),
            "",
            "# operators",
        ] + bpyx.ops_names(Globals.addon_key) +
        [
            "",
            "# core logic",
            f"import {__package__}.core as swv_core"
        ]
    )
    return comment + "\n" + code
def data_get_or_create(text_name: str) -> DataPropertyGroup:
    data: DataPropertyGroup
    if text_name in bpy.data.texts:
        text = bpy.data.texts.get(text_name)
        data = getattr(text, Globals.data_key)
    else:
        text = bpy.data.texts.new(text_name)
        data = data_get(text_name)
        data.templates_get().add()
        text.write(info_code_get(data))
    return data
def data_parse(data: DataPropertyGroup = None):
    file_path = bpyx.file_path_get()
    file_stem = file_path.stem
    template = data.template_core_get()
    if config.log: logger.debug(template)
    parts = core.parse(file_stem, template)
    if config.log: logger.debug(parts)
    data.root = parts.root
    data.version_value = core.version_str(parts.version)
def data_update(
        text_name: str,
        should_load_all_files: bool,
):
    preferences = Preferences.instance_get()
    data = data_get(text_name)
    if data is None:
        return
    file_path = bpyx.file_path_get()
    data_parse(data)
    for template in data.templates_get():
        template.files.clear()
        directory_path = Path(bpy.path.abspath(template.dirpath))
        if not preferences.should_load_all_files_get() and data.root:
            pattern = f"*{data.root}*.blend"
        else:
            pattern = "*.blend"
        paths = list(directory_path.glob(pattern))
        for path in paths:
            item: FilePathProperties = template.files.add()
            item.path = str(path)
            item.stem = path.stem
        try:
            template.files_active_index = paths.index(file_path)
        except ValueError:
            template.files_active_index = 0
def data_templates_get_or_create() -> bpyx.PropCollection[TemplateProperties]:
    preferences = Preferences.instance_get()
    text_name = preferences.text_name_get()
    data = data_get_or_create(text_name)
    templates = data.templates
    return templates
@bpy.app.handlers.persistent
@bpyx.addon_setup.handler(bpy.app.handlers.save_pre)
def data_update_handler(filepath: str):
    if filepath:
        preferences = Preferences.instance_get()
        text_name = preferences.text_name_get()
        should_load_all_files = preferences.should_load_all_files_get()
        data_update(text_name, should_load_all_files)
        if config.log: logger.debug(f"updated {repr(filepath)}")
    else:  # startup file
        if config.log: logger.debug("no file path")
