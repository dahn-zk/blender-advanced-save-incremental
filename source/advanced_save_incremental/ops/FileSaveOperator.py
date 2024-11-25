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

from pathlib import Path

import bpy

from .. import bpyx
from ..prefs import config
from ..props.FileSaveOperatorProps import FileSaveOperatorProps
from ..props.Props import logger
from ..props.TemplateProps import TemplateProps
from .BasePathOperator import BasePathOperator

@bpyx.addon_setup.registree
class FileSaveOperator(BasePathOperator):
    bl_idname = f"{config.addon_key}.save"
    bl_label = config.addon_name
    bl_options = {'REGISTER'}
    ui_icon = 'FILE_TICK'
    #
    dirpath: TemplateProps.dirpath_def
    filename: FileSaveOperatorProps.filename_def
    save_copy: TemplateProps.save_copy_def
    save_overwrite: TemplateProps.save_overwrite_def
    #
    def execute(self, context: bpy.types.Context):
        try:
            self.path = Path(bpy.path.abspath(self.dirpath))
            self.path_create_directory()
            self.path /= self.filename
            #
            if config.log: logger.debug(f"saving as {repr(self.path)}")
            bpy.ops.wm.save_mainfile()
            if not self.save_overwrite and self.path.exists():
                # changing context for file dialog when file already exists https://projects.blender.org/blender/blender/issues/104804
                # noinspection PyTypeChecker
                bpy.ops.wm.save_as_mainfile(
                    'INVOKE_DEFAULT',
                    filepath = str(self.path),
                    copy = self.save_copy,
                    check_existing = True,
                )
            else:
                bpy.ops.wm.save_as_mainfile(
                    filepath = str(self.path),
                    copy = self.save_copy,
                )
            # trigger update (via save_pre handler) to refresh file openers
            bpy.ops.wm.save_mainfile()
        except Exception as exc:
            self.report_exception_current(f"{repr(self.path)}")
            logger.error(f"could not save {self.path}\n", exc_info = exc)
        return {'FINISHED'}
    #
    @classmethod
    def description(cls, context, properties):
        sentences = []
        if properties.get(TemplateProps.save_copy_key):
            # copy of native "Save Copy" operator's description
            sentences.append("Save a copy of the current working state and do not make saved file active")
        if properties.get(TemplateProps.save_overwrite_key):
            sentences.append("Save and overwrite an existing file without warning")
        if len(sentences) == 0:
            sentences.append("Save the current file at the specified path")
        details = (f'"{properties.get(FileSaveOperatorProps.filename_key)}" '
                   f'in "{properties.get(TemplateProps.dirpath_key)}"')
        return ". ".join(sentences) + ".\n" + details
