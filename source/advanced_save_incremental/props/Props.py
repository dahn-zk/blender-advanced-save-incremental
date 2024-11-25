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

import bpy

from .. import bpyx
from .. import config
from .. import core
from ..prefs.Preferences import Preferences
from .info import info_code_get
from .TemplateProps import TemplateProps

logger = logging.getLogger(__name__)

props_key = f"{config.addon_key}_data"

@bpyx.addon_setup.registree
@bpyx.addon_setup.custom_property_pointer(bpy.types.Text, props_key)
class Props(bpy.types.PropertyGroup):
    """ all add-on's data for a blend-file """
    #
    def _update(self, value):
        props_parse(self)
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
        if value: self[Props.version_separator_key] = value
    def version_separator_get(self) -> str:
        return self.get(Props.version_separator_key, ".")
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
    def version_template_get(self):
        return core.VersionTemplate(
            separator = self.version_separator,
            count = self.version_count,
            width = 0,
        )
    #
    ### computed properties
    root_key = "root"
    root: bpy.props.StringProperty(
        name = "Root",
        description = "File name part without version and affixes",
    )

    def root_get(self) -> str:
        return self.root
    #
    version_str_key = "version_str"
    version_str: bpy.props.StringProperty(
        name = "Version",
        description = "File name part containing only version",
    )
    def version_str_get(self) -> str:
        return self.version_str
    #
    ### other properties and UI state
    def version_parts_get(self):
        version_str = self.version_str_get()
        version_template = self.version_template_get()
        version_str_parts = version_str.split(version_template.separator)
        return [int(e) for e in version_str_parts if e.isnumeric()]
    #
    def template_core_get(self):
        return core.Template(
            name = self.name,
            prefix = self.prefix,
            suffix = self.suffix,
            version = self.version_template_get(),
        )
    #
    templates_key = "templates"
    templates_def = bpy.props.CollectionProperty(
        name = "Templates",
        type = TemplateProps,
    )
    templates: templates_def
    def templates_get(self) -> bpyx.PropCollection[TemplateProps]:
        return self.templates
    #
    ui_show_template_key = "ui_show_template"
    ui_show_template_def = bpy.props.BoolProperty(
        name = "Show Template",
        default = True,
        description = "How the current file is named"
    )
    ui_show_template: ui_show_template_def
    #
    ui_list_buttons_key = "ui_list_buttons"
    ui_list_buttons_def = bpy.props.BoolProperty(
        name = "Show List Operators",
        default = True,
    )
    ui_list_buttons: ui_list_buttons_def

def props_get(text_name: str = None) -> Props | None:
    if text_name is None:
        text_name = Preferences.instance_get().text_name_get()
    datablock = bpy.data.texts.get(text_name)
    if datablock is None:
        return None
    else:
        return getattr(datablock, props_key, None)

def props_get_or_crt(text_name: str = None) -> Props:
    if text_name is None:
        text_name = Preferences.instance_get().text_name_get()
    props: Props
    if text_name in bpy.data.texts:
        text = bpy.data.texts.get(text_name)
        props = getattr(text, props_key)
    else:
        text = bpy.data.texts.new(text_name)
        props = props_get(text_name)
        props.templates_get().add()
        text.write(info_code_get(props))
    return props

def props_del():
    text_name = Preferences.instance_get().text_name_get()
    datablock = bpy.data.texts.get(text_name)
    if datablock is not None:
        bpy.data.texts.remove(datablock)

def props_parse(props: Props = None):
    if props is None:
        props = props_get_or_crt()
    file_path = bpyx.file_path_get()
    file_stem = file_path.stem
    template = props.template_core_get()
    if config.log: logger.debug(template)
    parts = core.parse_stem(file_stem, template)
    if config.log: logger.debug(parts)
    props.root = parts.root
    props.version_str = core.build.version_str(parts.version)

def props_update(text_name: str = None):
    if text_name is None:
        text_name = Preferences.instance_get().text_name_get()
    props = props_get(text_name)
    if props is None: return
    file_path = bpyx.file_path_get()
    props_parse(props)
    root = props.root_get()
    version_parts = props.version_parts_get()
    for template in props.templates_get():
        template.update(root, version_parts)

def props_templates_get_or_crt() -> bpyx.PropCollection[TemplateProps]:
    props = props_get_or_crt()
    templates = props.templates
    return templates

@bpy.app.handlers.persistent
@bpyx.addon_setup.handler(bpy.app.handlers.save_pre)
def save_pre(filepath: str):
    if filepath:
        props_update()
        if config.log: logger.debug(f"updated {repr(filepath)}")
    else:  # startup file
        if config.log: logger.debug("no file path")
