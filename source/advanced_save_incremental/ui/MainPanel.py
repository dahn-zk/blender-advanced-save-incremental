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

from ..exts import bpyx
from ..exts import stdx
from ..ops.DeleteOperator import DeleteOperator
from ..ops.HelpOperator import HelpOperator
from ..prefs import config
from ..prefs.Preferences import Preferences
from ..props.Props import props_get
from ..props.Props import Props
from ..props.FilePathProps import FilePathProps
from ..props.TemplateProps import TemplateProps
from ..props.VersionTemplateProps import VersionTemplateProps
from ..ops.CreateOrUpdateOperator import CreateOrUpdateOperator
from ..ops.FileSaveOperator import FileSaveOperator
from ..ops.TemplatesAddOperator import TemplatesAddOperator
from ..ops.TemplateMoveOperator import TemplateMoveOperator
from ..ops.TemplatesPersistenceOperator import TemplatesImportOperator
from ..ops.TemplatesPersistenceOperator import TemplatesExportOperator
from ..ops.TemplatesRemoveAllOperator import TemplatesRemoveAllOperator
from ..ops.TemplatesRemoveOperator import TemplatesRemoveOperator
from .FilesList import ASI_UL_files

def draw_template_parts_toggle(
        layout: bpy.types.UILayout,
        template: TemplateProps,
):
    row = layout.row(heading = "Use")
    row.prop(template, TemplateProps.prefix_use_key, text = "Prefix", toggle = True)
    row.prop(template, TemplateProps.suffix_use_key, text = "Suffix", toggle = True)
    row.prop(template, TemplateProps.version_use_key, text = "Version", toggle = True)

def draw_template_version(
        layout: bpy.types.UILayout,
        version_template: VersionTemplateProps,
):
    layout.label(text = f"Version")
    layout.prop(version_template, VersionTemplateProps.count_key)
    if version_template.count > 1:
        layout.prop(version_template, VersionTemplateProps.separator_key)
    layout.prop(version_template, VersionTemplateProps.width_key)

def draw_template_save_toggle(
        layout: bpy.types.UILayout,
        template: TemplateProps,
):
    row = layout.row(heading = "Save")
    row.prop(template, TemplateProps.save_copy_key, toggle = True)
    row.prop(template, TemplateProps.save_overwrite_key, toggle = True)

def draw_template_core(
        layout: bpy.types.UILayout,
        template: TemplateProps,
):
    layout.use_property_split = True
    # dirpath
    layout.prop(template, TemplateProps.dirpath_key)
    # parts settings
    draw_template_parts_toggle(layout, template)
    # parts values
    if template.prefix_use:
        layout.prop(template, TemplateProps.prefix_key)
    if template.suffix_use:
        layout.prop(template, TemplateProps.suffix_key)
    if template.version_use:
        draw_template_version(layout.box(), template.version)
    # buttons settings
    draw_template_save_toggle(layout, template)
    layout.use_property_split = False

def draw_template_save_buttons(
        layout: bpy.types.UILayout,
        template: TemplateProps,
):
    for file_save_data in template.saves_datas_get():
        op = FileSaveOperator.drawx(layout, text = file_save_data.label_get())
        op.dirpath = template.dirpath
        op.filename = file_save_data.file_name_get()
        op.save_copy = template.save_copy
        op.save_overwrite = template.save_overwrite

def draw_template_files_list(
        layout: bpy.types.UILayout,
        template: TemplateProps,
        template_idx: int,
        files_list_rows_max: int,
        files_list_rows_min: int,
):
    header_row = layout.row(align = True)
    header_subrow = header_row.row()  # alignment trickery
    header_subrow.alignment = 'LEFT'
    bpyx.draw_opening_arrow(header_subrow, template,
        key = TemplateProps.ui_show_files_key, text = "Files Openers")
    data_update_row = header_row.row()
    data_update_row.alignment = 'RIGHT'
    data_update_row.label()  # please don't ask me why
    if template.ui_show_files:
        CreateOrUpdateOperator.drawx(data_update_row)
        list_row = layout.row()
        list_row.separator()  # just a small gap for aesthetics
        cls_name = ASI_UL_files.__name__
        list_rows_count = min(files_list_rows_max, len(template.files))
        list_row.template_list(
            listtype_name = cls_name,
            list_id = f"{cls_name}_{template_idx}",
            dataptr = template,
            propname = TemplateProps.files_key,
            active_dataptr = template,
            active_propname = TemplateProps.files_active_index_key,
            item_dyntip_propname = FilePathProps.path_key,
            rows = max(files_list_rows_min, list_rows_count),
            maxrows = files_list_rows_max,
        )

def draw_template_operators(
        layout: bpy.types.UILayout,
        template_idx: int,
):
    row = layout.row()
    # remove
    opr: TemplatesRemoveOperator
    opr = TemplatesRemoveOperator.drawx(row)
    opr.index = template_idx
    # move up/down
    split = row.split(align = True)
    for icon, delta in [('TRIA_UP', -1), ('TRIA_DOWN', 1)]:
        opm: TemplateMoveOperator
        opm = TemplateMoveOperator.drawx(split, icon = icon, text = "")
        opm.index = template_idx
        opm.delta = delta

def draw_templates(
        layout: bpy.types.UILayout,
        templates: bpyx.PropCollection[TemplateProps],
        version_parts: list[int],
        ui_list_buttons: bool,
        files_should_show: bool,
        files_list_rows_min = 0, files_list_rows_max = 0,
):
    layout.row().label(text = "Save Templates")
    template: TemplateProps  # fix PyCharm issue with `enumerate` typings
    for template_idx, template in enumerate(templates):
        template_box = layout.box()
        # header
        template_header_row = template_box.row(align = True)
        bpyx.draw_opening_arrow(template_header_row, template,
            key = TemplateProps.ui_opened_key)
        template_header_row.prop(template, "name", text = "")
        # core properties
        if template.ui_opened:
            draw_template_core(template_box, template)
        # save buttons
        draw_template_save_buttons(template_box, template)
        # files openers
        if files_should_show:
            draw_template_files_list(template_box, template, template_idx,
                files_list_rows_max, files_list_rows_min)
        # collection operators
        if ui_list_buttons:
            draw_template_operators(template_box, template_idx)

def draw_templates_operators(layout: bpy.types.UILayout):
    TemplatesRemoveAllOperator.drawx(layout)
    TemplatesAddOperator.drawx(layout)

@bpyx.addon_setup.registree
class MainPanel(bpy.types.Panel, stdx.SafeCallMixIn):
    # note that the bl_idname must be this way (with _PT_ infix) as for 4.2
    bl_idname = f"{config.addon_key.upper()}_PT_main"
    bl_label = config.addon_name
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = bl_label
    bl_order = 3
    #
    def _draw_intro(self, layout: bpy.types.UILayout):
        row = layout.row(align = True)
        row.alignment = 'RIGHT'
        bpyx.ui.draw_op_preferences_addon_show(row, config.addon_package)
        HelpOperator.drawx(row)
        layout.separator(type = 'LINE')
    def _draw_data_create(self, layout: bpy.types.UILayout):
        layout.label(icon = 'INFO', text = "No local templates")
        CreateOrUpdateOperator.drawx(layout, text = "Create Templates", icon = 'ADD')
    def _draw_file_data(self, layout: bpy.types.UILayout, data: Props):
        layout.use_property_split = True
        header = layout.row()
        header.label(text = f"Current File: {bpyx.file_path_get().stem}")
        CreateOrUpdateOperator.drawx(header)
        # template
        template_box = layout.box()
        template_box.use_property_split = False
        template_header_box = template_box.row()
        template_header_box.alignment = 'LEFT'
        bpyx.draw_opening_arrow(template_header_box, data,
            key = Props.ui_show_template_key, text = "Naming Pattern")
        template_box.use_property_split = True
        if data.ui_show_template:
            template_box.prop(data, Props.prefix_key)
            template_box.prop(data, Props.suffix_key)
            template_box.prop(data, Props.version_count_key)
            if data.version_count > 1:
                template_box.prop(data, Props.version_separator_key)
        #
        layout.prop(data, Props.root_key, emboss = False)
        layout.prop(data, Props.version_str_key, emboss = False)
    def _draw_advanced_section(self, layout: bpy.types.UILayout, data: Props):
        layout.separator(type = 'LINE')
        layout.prop(data, Props.ui_list_buttons_key)
        TemplatesImportOperator.drawx(layout)
        TemplatesExportOperator.drawx(layout)
        layout.separator(type = 'LINE')
        row = layout.row()
        row.alignment = 'RIGHT'
        DeleteOperator.drawx(row, text = "")
    def _safe_call(self, context: bpy.types.Context):
        layout = self.layout
        preferences = Preferences.instance_get()
        main = props_get(preferences.text_name_get())
        # intro
        if preferences.should_show_intro_buttons_get():
            self._draw_intro(layout)
        # if data not created yet
        if main is None:
            self._draw_data_create(layout.box())
            return
        # current file info
        self._draw_file_data(layout.box(), main)
        # templates
        templates_box = layout.box()
        draw_templates(layout = templates_box,
            templates = main.templates_get(),
            version_parts = main.version_parts_get(),
            ui_list_buttons = main.ui_list_buttons,
            files_should_show = preferences.should_show_file_openers_get(),
            files_list_rows_min = preferences.file_list_rows_min_get(),
            files_list_rows_max = preferences.file_list_rows_max_get())
        if main.ui_list_buttons:
            draw_templates_operators(templates_box.row())
        #
        self._draw_advanced_section(layout, main)
    def draw(self, context: bpy.types.Context):
        self.safe_call(context)
