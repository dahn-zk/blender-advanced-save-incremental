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
from . import config

@bpyx.addon_setup.registree
class Preferences(stdx.SafeCallMixIn, bpyx.AddonPreferences):
    #
    bl_idname = config.addon_package
    #
    should_show_file_openers_key = "should_show_file_openers"
    should_show_file_openers_def = bpy.props.BoolProperty(
        name = "Show",
        default = True,
        description = "Show the file openers in the templates.",
    )
    should_show_file_openers: should_show_file_openers_def
    def should_show_file_openers_get(self) -> bool:
        return self.should_show_file_openers
    #
    should_load_all_files_key = "should_load_all_files"
    should_load_all_files_def = bpy.props.BoolProperty(
        name = "Load All Files",
        default = True,
        description = (
            "Load all Blender files instead of only those which match the "
            "current stem root"),
    )
    should_load_all_files: should_load_all_files_def
    def should_load_all_files_get(self) -> bool:
        return self.should_load_all_files
    #
    file_list_rows_min_key = "file_list_rows_min"
    file_list_rows_min_def = bpy.props.IntProperty(
        name = "Min Rows",
        default = 2,
        min = 1, max = 10,
        description = "Minimum number of rows in the file openers",
    )
    file_list_rows_min: file_list_rows_min_def
    def file_list_rows_min_get(self) -> int:
        return self.file_list_rows_min
    #
    file_list_rows_max_key = "file_list_rows_max"
    file_list_rows_max_def = bpy.props.IntProperty(
        name = "Max Rows",
        default = 8,
        min = 1,
        max = 20,
        description = "Maximum number of rows in the file openers",
    )
    file_list_rows_max: file_list_rows_max_def
    def file_list_rows_max_get(self) -> int:
        return self.file_list_rows_max
    #
    file_items_emboss_key = "file_items_emboss"
    file_items_emboss_def = bpy.props.BoolProperty(
        name = "Display Files as Buttons",
        default = True,
        description = (
            "Emboss the file items to make them look like buttons. This is "
            "enabled for the first-time users to illustrate that when clicking "
            "on the empty space in the row, the file won't open - it only opens "
            "when clicking on the text, and there is no way to configure the "
            "hitbox to occupy the whole row. This is a limitation in Blender API, "
            "and hopefully it will be fixed in the future"),
    )
    file_items_emboss: file_items_emboss_def
    def file_items_emboss_get(self) -> bool:
        return self.file_items_emboss
    #
    text_name_key = "text_name"
    text_name_def = bpy.props.StringProperty(
        name = "Datablock Name",
        default = f".{config.addon_key}.data.py",
        description = (
            "Name of the Text datablock where to save the add-on's data to"),
    )
    text_name: text_name_def
    def text_name_get(self) -> str:
        return self.text_name
    #
    should_show_intro_buttons_key = "should_show_intro_buttons"
    should_show_intro_buttons_def = bpy.props.BoolProperty(
        name = "Show Intro Buttons",
        default = True,
        description = "Show the introductory buttons in the header of the add-on's panel",
    )
    should_show_intro_buttons: should_show_intro_buttons_def
    def should_show_intro_buttons_get(self) -> bool:
        return self.should_show_intro_buttons
    #
    def _safe_call(self, context: bpy.types.Context):
        layout = self.layout
        layout.use_property_split = True
        col_files = layout.column(heading = "Files Openers", align = True)
        col_files.prop(self, Preferences.should_show_file_openers_key)
        if self.should_show_file_openers_get():
            col_files.prop(self, Preferences.should_load_all_files_key)
            col_files.prop(self, Preferences.file_list_rows_min_key)
            col_files.prop(self, Preferences.file_list_rows_max_key)
            col_files.prop(self, Preferences.file_items_emboss_key)
        layout.prop(self, Preferences.text_name_key)
        layout.prop(self, Preferences.should_show_intro_buttons_key)
    def draw(self, context: bpy.types.Context):
        self.safe_call(context)
