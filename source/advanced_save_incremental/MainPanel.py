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
from . import stdx
from .bpyx import file_path_get
from .DataPropertyGroup import data_get
from .DataPropertyGroup import DataPropertyGroup
from .DataUpdateOperator import DataUpdateOperator
from .FilePathProperties import FilePathProperties
from .FileSaveOperator import FileSaveOperator
from .FilesUIList import SAVE_WITH_VERSION_UL_files
from .Globals import Globals
from .Preferences import Preferences
from .StoredTemplateProperties import StoredTemplateProperties
from .TemplateMoveOperator import TemplateMoveOperator
from .TemplateProperties import TemplateProperties
from .TemplatesAddOperator import TemplatesAddOperator
from .TemplatesRemoveAllOperator import TemplatesRemoveAllOperator
from .TemplatesRemoveOperator import TemplatesRemoveOperator
from .VersionParseOperator import VersionParseOperator
from .VersionTemplatePropertyGroup import VersionTemplatePropertyGroup

def draw_template_core(layout: bpy.types.UILayout, template: TemplateProperties):
    layout.use_property_split = True
    layout.prop(template, TemplateProperties.dirpath_key)
    # parts settings
    parts_row = layout.row(heading = "Use")
    for key, text in [
        [TemplateProperties.prefix_use_key, "Prefix"],
        [TemplateProperties.suffix_use_key, "Suffix"],
        [TemplateProperties.version_use_key, "Version"],
    ]:
        parts_row.prop(template, key, text = text, toggle = True)
    # parts values
    if template.prefix_use:
        layout.prop(template, TemplateProperties.prefix_key)
    if template.suffix_use:
        layout.prop(template, TemplateProperties.suffix_key)
    if template.version_use:
        version_box = layout.box()
        version_box.label(text = f"Version")
        version_box.prop(template.version, VersionTemplatePropertyGroup.count_key)
        if template.version.count > 1:
            version_box.prop(template.version, VersionTemplatePropertyGroup.separator_key)
        version_box.prop(template.version, VersionTemplatePropertyGroup.width_key)
    # buttons settings
    row_save_settings = layout.row(heading = "Save")
    row_save_settings.prop(template, TemplateProperties.save_copy_key, toggle = True)
    row_save_settings.prop(template, TemplateProperties.save_overwrite_key, toggle = True)
    layout.use_property_split = False
def draw_template_save_button(
        layout: bpy.types.UILayout,
        template: TemplateProperties,
        text: str,
):
    op = FileSaveOperator.draw_layout(layout, text = text)
    op.dirpath = template.dirpath
    op.prefix_use = template.prefix_use
    op.prefix = template.prefix
    op.suffix_use = template.suffix_use
    op.suffix = template.suffix
    op.version_use = template.version_use
    if op.version_use:
        version_template = template.version_get()
        op.version_separator = version_template.separator
        op.version_count = version_template.count
        op.version_width = version_template.width
    op.save_copy = template.save_copy
    op.save_overwrite = template.save_overwrite
def draw_template_save_incremental_button(
        layout: bpy.types.UILayout,
        template: TemplateProperties,
        phrase: str,
        version: core.Version,
        version_part_idx: int,
):
    version_template = template.version_get()
    core.version_inc(version, version_part_idx, version_template.count)
    version_value = core.version_str(version)
    text = phrase
    if version_template.count == 1:
        text += f" Incremental: {version_value}"
    else:
        version_part_name = core.VersionTemplate.config.parts[version_part_idx]
        text += f" with Incremented {version_part_name}: {version_value}"
    op: FileSaveOperator
    op = FileSaveOperator.draw_layout(layout, text = text)
    op.dirpath = template.dirpath
    op.prefix_use = template.prefix_use
    op.prefix = template.prefix
    op.suffix_use = template.suffix_use
    op.suffix = template.suffix
    op.version_increment = True
    op.version_use = template.version_use
    op.version_separator = version_template.separator
    op.version_count = version_template.count
    op.version_width = version_template.width
    op.version_is_preset = True
    op.version_preset = version_value
    op.save_copy = template.save_copy
    op.save_overwrite = template.save_overwrite
def draw_template_save_buttons(
        layout: bpy.types.UILayout,
        template: TemplateProperties,
        version_parts: list[int],
):
    # non-versioned save
    phrase = "Overwrite" if template.save_overwrite else "Save"
    if template.save_copy: phrase += " Copy"
    col = layout.column()
    draw_template_save_button(col, template, phrase)
    # incremental save
    version_template = template.version_get()
    if template.version_use:
        for version_part_idx in range(version_template.count):
            core_version_template = version_template.core_get()
            version_parts = version_parts[:version_template.count]
            version = core.Version(version_parts, core_version_template)
            draw_template_save_incremental_button(col, template, phrase,
                version, version_part_idx)
def draw_template_files_list(
        layout: bpy.types.UILayout,
        template: StoredTemplateProperties,
        template_idx: int,
        files_list_rows_max: int,
        files_list_rows_min: int,
):
    header_row = layout.row(align = True)
    header_subrow = header_row.row()  # alignment trickery
    header_subrow.alignment = 'LEFT'
    bpyx.draw_opening_arrow(header_subrow, template,
        key = StoredTemplateProperties.ui_show_files_key, text = "Files")
    data_update_row = header_row.row()
    data_update_row.alignment = 'RIGHT'
    data_update_row.label()  # please don't ask me why
    DataUpdateOperator.draw_layout(data_update_row, text = "")
    if template.ui_show_files:
        list_row = layout.row()
        list_row.separator()  # just a small gap for aesthetics
        cls_name = SAVE_WITH_VERSION_UL_files.__name__
        list_rows_count = min(files_list_rows_max, len(template.files))
        list_row.template_list(
            listtype_name = cls_name,
            list_id = f"{cls_name}_{template_idx}",
            dataptr = template,
            propname = StoredTemplateProperties.files_key,
            active_dataptr = template,
            active_propname = StoredTemplateProperties.files_active_index_key,
            item_dyntip_propname = FilePathProperties.path_key,
            rows = max(files_list_rows_min, list_rows_count),
            maxrows = files_list_rows_max,
        )
def draw_template_operators(layout: bpy.types.UILayout, template_idx: int):
    row = layout.row()
    # remove
    opr: TemplatesRemoveOperator
    opr = TemplatesRemoveOperator.draw_layout(row)
    opr.index = template_idx
    # move up/down
    split = row.split(align = True)
    for icon, delta in [('TRIA_UP', -1), ('TRIA_DOWN', 1)]:
        opm: TemplateMoveOperator
        opm = TemplateMoveOperator.draw_layout(split, icon = icon, text = "")
        opm.index = template_idx
        opm.delta = delta
def draw_templates(
        layout: bpy.types.UILayout,
        templates: bpyx.PropCollection[TemplateProperties],
        version_parts: list[int],
        ui_list_buttons: bool,
        files_list_rows_min = 0, files_list_rows_max = 0,
):
    layout.row().label(text = "Save Templates")
    for template_idx, template in enumerate(templates):
        template: StoredTemplateProperties  # fix PyCharm issue with enumerate typings
        template_box = layout.box()
        # header
        template_header_row = template_box.row(align = True)
        bpyx.draw_opening_arrow(template_header_row, template,
            key = StoredTemplateProperties.ui_opened_key)
        template_header_row.prop(template, "name", text = "")
        # core properties
        if template.ui_opened:
            draw_template_core(template_box, template)
        # save buttons
        draw_template_save_buttons(template_box, template, version_parts)
        # files list
        draw_template_files_list(template_box, template, template_idx,
            files_list_rows_max, files_list_rows_min)
        # operators
        if ui_list_buttons:
            draw_template_operators(template_box, template_idx)
def draw_templates_operators(layout: bpy.types.UILayout):
    TemplatesRemoveAllOperator.draw_layout(layout)
    TemplatesAddOperator.draw_layout(layout)

@bpyx.addon_setup.registree
class MainPanel(bpy.types.Panel, stdx.SafeCaller):
    # note that the bl_idname must be this way (with _PT_ infix) as for 4.2
    bl_idname = f"{Globals.addon_key.upper()}_PT_main"
    bl_label = "Save"
    bl_space_type = 'VIEW_3D'  # 3D Viewort
    bl_region_type = 'UI'  # Sidebar ("N-panel")
    bl_category = bl_label
    bl_order = 3
    #
    def _draw_header(self, layout):
        layout.label(
            text = f"Add-on: {Globals.addon_name} v{Globals.addon_version}")
        layout.operator("preferences.addon_show",
            icon = 'PREFERENCES', text = "").module = __package__
    def _draw_data_create(self, layout):
        row = layout.row()
        row.label(icon = 'INFO',
            text = "No data have been set yet for the current file.")
        DataUpdateOperator.draw_layout(layout, text = "Create")
    def _draw_file_data(self, data: DataPropertyGroup, layout):
        layout.use_property_split = True
        header = layout.row()
        header.label(text = f"Current File: {file_path_get().stem}")
        VersionParseOperator.draw_layout(header, text = "")
        # template
        template_box = layout.box()
        template_box.use_property_split = False
        template_header_box = template_box.row()
        template_header_box.alignment = 'LEFT'
        bpyx.draw_opening_arrow(template_header_box, data,
            key = DataPropertyGroup.ui_show_template_key, text = "Template")
        template_box.use_property_split = True
        if data.ui_show_template:
            template_box.prop(data, DataPropertyGroup.prefix_key)
            template_box.prop(data, DataPropertyGroup.suffix_key)
            template_box.prop(data, DataPropertyGroup.version_count_key)
            if data.version_count > 1:
                template_box.prop(data, DataPropertyGroup.version_separator_key)
        #
        layout.prop(data, DataPropertyGroup.root_key, emboss = False)
        layout.prop(data, data.version_value_key, emboss = False)
    def _safe_call(self, context: bpy.types.Context):
        layout = self.layout
        preferences = Preferences.instance_get()
        data = data_get(preferences.text_name_get())
        # header
        self._draw_header(layout.row())
        layout.separator(type = 'LINE')
        # if data not created yet
        if data is None:
            self._draw_data_create(layout.box())
            return
        # current file info
        self._draw_file_data(data, layout.box())
        # templates
        templates_box = layout.box()
        draw_templates(layout = templates_box,
            templates = data.templates_get(),
            version_parts = data.version_parts_get(),
            ui_list_buttons = data.ui_list_buttons,
            files_list_rows_min = preferences.file_list_rows_min_get(),
            files_list_rows_max = preferences.file_list_rows_max_get())
        if data.ui_list_buttons:
            draw_templates_operators(templates_box.row())
        #
        layout.prop(data, DataPropertyGroup.ui_list_buttons_key)
    def draw(self, context: bpy.types.Context):
        self.safe_call(context)
