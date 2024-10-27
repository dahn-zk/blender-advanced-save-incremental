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

from . import bpyx
from . import config
from . import core
from .BasePathOperator import BasePathOperator
from .DataPropertyGroup import data_get
from .DataPropertyGroup import data_parse
from .DataPropertyGroup import logger
from .Globals import Globals
from .Preferences import Preferences
from .TemplateProperties import TemplateProperties
from .VersionTemplatePropertyGroup import VersionTemplatePropertyGroup

@bpyx.addon_setup.registree
class FileSaveOperator(BasePathOperator):
    bl_idname = f"{Globals.addon_key}.save"
    bl_label = Globals.addon_name
    bl_options = {'REGISTER'}
    icon = 'FILE_TICK'
    #
    dirpath: TemplateProperties.dirpath_def
    #
    prefix_use: TemplateProperties.prefix_use_def
    prefix: TemplateProperties.prefix_def
    #
    suffix_use: TemplateProperties.suffix_use_def
    suffix: TemplateProperties.suffix_def
    #
    version_use: TemplateProperties.version_use_def
    version_increment: bpy.props.BoolProperty(name = "Increment Version")
    version_separator: VersionTemplatePropertyGroup.separator_def
    version_count: VersionTemplatePropertyGroup.count_def
    version_width: VersionTemplatePropertyGroup.width_def
    version_increment_index: bpy.props.IntProperty(name = "Version Index",
        min = 0, max = (len(core.VersionTemplate.config.parts) - 1))
    version_is_preset_key = "version_is_preset"
    version_is_preset: bpy.props.BoolProperty(name = "Preset Version",
        default = False,
        description = (
            "Ignore version template parameters if any and use preset version "
            "value instead"))
    version_preset: bpy.props.StringProperty(name = "Version",
        description = f"See {version_is_preset_key}")
    #
    save_copy: TemplateProperties.save_copy_def
    save_overwrite: TemplateProperties.save_overwrite_def
    #
    def execute(self, context: bpy.types.Context):
        try:
            self._execute()
        except OSError as exc:
            self.report_invalid_input(f"Could not save the file due to an OS error: {exc}")
            logger.error("could not save due to an OS error", exc_info = exc)
            return {'CANCELLED'}
        except Exception as exc:
            self.report_exception_current(f"{repr(self.path)}")
            return {'CANCELLED'}
        return {'FINISHED'}
    def _execute(self):
        data = data_get(Preferences.instance_get().text_name_get())
        data_parse(data)
        #
        prefix = self.prefix if self.prefix_use else ""
        suffix = self.suffix if self.suffix_use else ""
        #
        # there is a minor problem with some code duplication between here and
        # MainPanel drawing code, but it allows to use this operator independently
        if not self.version_use:
            version_value = ""
        elif self.version_is_preset:
            version_value = self.version_preset
        else:
            version = core.Version(
                parts = data.version_parts_get(),
                template = core.VersionTemplate(
                    separator = self.version_separator,
                    count = self.version_count,
                    width = self.version_width,
                ),
            )
            if self.version_increment: core.version_inc(version,
                index = self.version_increment_index,
                count = self.version_count,
            )
            version_value = core.version_str(version)
        #
        name = f"{prefix}{data.root}{suffix}{version_value}.blend"
        #
        self.path = Path(bpy.path.abspath(self.dirpath))
        self.path.mkdir(parents = True, exist_ok = True)
        self.path /= name
        #
        if config.log: logger.debug(f"saving as {repr(self.path)}")
        bpy.ops.wm.save_mainfile()
        if not self.save_overwrite and self.path.exists():
            # changing context for file dialog when file already exists
            # https://projects.blender.org/blender/blender/issues/104804
            # broken typings in fake-bpy-module for this one
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
        # trigger update (via save_pre handler) to refresh file selectors lists
        bpy.ops.wm.save_mainfile()
    @classmethod
    def description(cls, context, properties):
        description = []
        if properties.get(TemplateProperties.save_copy_key):
            description.append("Save a copy of the current working state and "
                               "do not make saved file active")
        if properties.get(TemplateProperties.save_overwrite_key):
            description.append("Save and overwrite an existing file without warning")
        if len(description) == 0:
            description.append("Save the current file at the specified path")
        return ". ".join(description)
