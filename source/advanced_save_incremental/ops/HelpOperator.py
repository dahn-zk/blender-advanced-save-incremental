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
from ..prefs import config
from .BaseOperator import BaseOperator

@bpyx.addon_setup.registree
class HelpOperator(BaseOperator):
    bl_idname = f"{config.addon_key}.help"
    bl_label = "Help"
    url = config.addon_readme_url
    bl_description = f"Open README file in the browser. Add-on's version: {config.addon_version}"
    ui_icon = 'HELP'
    ui_text = ""
    def execute(self, context):
        bpy.ops.wm.url_open(url = self.url)
        return {'FINISHED'}
