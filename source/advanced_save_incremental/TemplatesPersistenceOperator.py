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

import tomllib
from pathlib import Path

import bpy.types

from . import bpyx
from .DataPropertyGroup import data_templates_get_or_create
from .TemplatesBaseOperator import TemplatesBaseOperator

class TemplatesPersistenceOperator(TemplatesBaseOperator):
    filepath: bpy.props.StringProperty(subtype = 'FILE_PATH')
    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.filepath = "templates.toml"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

@bpyx.addon_setup.registree
class TemplatesImportOperator(TemplatesPersistenceOperator):
    bl_idname = f"{TemplatesPersistenceOperator.idname}_import"
    bl_label = "Import Templates from TOML"
    icon = 'IMPORT'
    def execute(self, context: bpy.types.Context):
        with open(Path(bpy.path.abspath(self.filepath)), "rb") as file:
            try:
                templates_dicts = tomllib.load(file).get("templates")
            except tomllib.TOMLDecodeError as exc:
                self.report_error(f"TOML decoding error: {exc}")
                return {'CANCELLED'}
        if not templates_dicts:
            self.report_info("TOML file is empty, nothing to import")
            return {'CANCELLED'}
        templates = data_templates_get_or_create()
        for template_dict in templates_dicts:
            template = templates.add()
            template.from_dict(template_dict)
        return {'FINISHED'}

@bpyx.addon_setup.registree
class TemplatesExportOperator(TemplatesPersistenceOperator):
    bl_idname = f"{TemplatesPersistenceOperator.idname}_export"
    bl_label = "Export Templates to TOML"
    icon = 'EXPORT'
    def execute(self, context: bpy.types.Context):
        templates = data_templates_get_or_create()
        with open(Path(bpy.path.abspath(self.filepath)), "w") as file:
            for template in templates:
                file.write(f"[[templates]]\n{template.to_toml()}\n\n")
        return {'FINISHED'}
