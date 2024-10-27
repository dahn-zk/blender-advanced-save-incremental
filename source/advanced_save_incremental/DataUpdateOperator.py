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
from .DataPropertyGroup import data_get_or_create
from .DataPropertyGroup import data_update
from .Globals import Globals
from .Preferences import Preferences

@bpyx.addon_setup.registree
class DataUpdateOperator(BaseOperator):
    bl_idname = f"{Globals.addon_key}.data_update"
    bl_label = "Reload"
    bl_description = (
        f"Create or update {Globals.addon_qname} add-on data in the current file")
    icon = 'FILE_REFRESH'
    def execute(self, context):
        preferences = Preferences.instance_get()
        text_name = preferences.text_name_get()
        data_get_or_create(text_name)
        data_update(text_name, preferences.should_load_all_files_get())
        return {'FINISHED'}
