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

from . import bpyx
from .DataPropertyGroup import data_templates_get_or_create
from .TemplatesBaseOperator import TemplatesBaseOperator

@bpyx.addon_setup.registree
class TemplatesRemoveAllOperator(TemplatesBaseOperator):
    bl_idname = f"{TemplatesBaseOperator.idname}_remove_all"
    bl_label = "Remove All"
    icon = 'REMOVE'
    def execute(self, context):
        templates = data_templates_get_or_create()
        templates.clear()
        return {'FINISHED'}
