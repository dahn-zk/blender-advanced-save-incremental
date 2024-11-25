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
from .. import config
from .BasePathOperator import BasePathOperator

logger = logging.getLogger(__name__)

@bpyx.addon_setup.registree
class FileOpenOperator(BasePathOperator):
    bl_idname = f"{config.addon_key}.open"
    bl_label = "Open in Current/New Window"
    bl_description = "Open the Blender file, hold Ctrl to open in a new window"
    filepath_key = "filepath"
    filepath: bpy.props.StringProperty(subtype = "FILE_PATH")
    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.new_window = event.ctrl
        if not context.blend_data.is_dirty or self.new_window:
            result = self.execute(context)
        else:
            if config.log: logger.debug(f"recent edits have not been saved to disk. invoking confirmation")
            result = context.window_manager.invoke_confirm(self, event,
                title = f"{self.bl_label}: Discard changes?",
                message = "Current changes have not been saved to disk.",
                confirm_text = "Discard", icon = "QUESTION")
        return result
    def execute(self, context: bpy.types.Context):
        try:
            self.path = Path(bpy.path.abspath(self.filepath))
            if self.new_window:
                bpy.ops.file.external_operation(filepath = self.filepath, operation = "OPEN")
            else:
                bpy.ops.wm.open_mainfile(filepath = self.filepath, check_existing = False,
                    display_file_selector = False)
        except Exception as exc:
            self.report_exception_current(f"Could not open: {self.filepath}")
            logger.error(f"could not open {self.path}\n", exc_info = exc)
        return {'FINISHED'}
