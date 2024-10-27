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
from .FilePathProperties import FilePathProperties
from .TemplateProperties import TemplateProperties

@bpyx.addon_setup.registree
class StoredTemplateProperties(TemplateProperties):
    #
    files_key = "files"
    files: bpy.props.CollectionProperty(
        name = "Files",
        type = FilePathProperties,
    )
    #
    files_active_index_key = "files_active_index"
    files_active_index: bpy.props.IntProperty(
        name = "Active File Index",
    )  # required by the API
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
        default = True,
    )
