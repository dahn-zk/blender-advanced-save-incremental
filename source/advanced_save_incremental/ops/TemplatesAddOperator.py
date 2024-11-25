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

from .. import bpyx
from ..props.Props import props_templates_get_or_crt
from .TemplatesBaseOperator import TemplatesBaseOperator

@bpyx.addon_setup.registree
class TemplatesAddOperator(TemplatesBaseOperator):
    bl_idname = f"{TemplatesBaseOperator.idname}_add"
    bl_label = "Add"
    ui_icon = 'ADD'
    def execute(self, context):
        templates = props_templates_get_or_crt()
        template_index = len(templates)
        template = templates.add()
        template.name = f"Template {template_index + 1}"
        template.save_datas_update(None)
        return {'FINISHED'}
