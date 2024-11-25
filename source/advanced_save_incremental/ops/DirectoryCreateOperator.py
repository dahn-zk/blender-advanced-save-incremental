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

import logging
from pathlib import Path

import bpy

from .. import bpyx
from ..prefs import config
from .BasePathOperator import BasePathOperator

logger = logging.getLogger(__name__)

@bpyx.addon_setup.registree
class DirectoryCreateOperator(BasePathOperator):
    bl_idname = f"{config.addon_key}.create_directory"
    bl_label = "Create the Directory"
    bl_description = "Create the directory if it does not exist yet"
    dirpath: bpy.props.StringProperty(subtype = 'DIR_PATH')
    def execute(self, context):
        try:
            self.path = Path(bpy.path.abspath(self.dirpath))
            self.path_create_directory()
        except Exception as exc:
            self.report_exception_current(f"Could not create the directory: {self.dirpath}")
            logger.error(f"could not create directory at {self.path}\n", exc_info = exc)
        return {'FINISHED'}
