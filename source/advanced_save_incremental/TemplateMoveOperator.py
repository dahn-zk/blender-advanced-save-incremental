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
from .DataPropertyGroup import data_templates_get_or_create
from .Globals import Globals
from .TemplatesBaseOperator import TemplatesBaseOperator

@bpyx.addon_setup.registree
class TemplateMoveOperator(TemplatesBaseOperator):
    bl_idname = f"{Globals.addon_key}.templates_move"
    bl_label = "Move"
    bl_description = "Move the template in a templates list up or down"
    index_key = "index"
    index: bpy.props.IntProperty(name = "Index",
        description = "Index of the template to move")
    delta_key = "delta"
    delta: bpy.props.IntProperty(name = "Delta",
        description = "How far to move the template")
    def execute(self, context):
        templates = data_templates_get_or_create()
        templates.move(self.index, self.index + self.delta)
        return {'FINISHED'}
