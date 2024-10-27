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
from .BaseOperator import BaseOperator
from .DataPropertyGroup import data_get
from .DataPropertyGroup import data_parse
from .Globals import Globals
from .Preferences import Preferences

@bpyx.addon_setup.registree
class VersionParseOperator(BaseOperator):
    bl_idname = f"{Globals.addon_key}.version_parse"
    bl_label = "Detect Version"
    bl_description = (
        "Detect a version of the current file based on the specified template")
    icon = 'FILE_REFRESH'
    def execute(self, context):
        data_parse(data_get(Preferences.instance_get().text_name_get()))
        return {'FINISHED'}
