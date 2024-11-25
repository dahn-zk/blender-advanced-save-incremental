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

from .. import bpyx
from ..props.Props import props_templates_get_or_crt
from .TemplatesBaseOperator import TemplatesBaseOperator

class TemplatesPersistenceOperator(TemplatesBaseOperator):
    filepath: bpy.props.StringProperty(subtype = 'FILE_PATH')
    format: bpy.props.EnumProperty(
        name = "Format",
        items = [
            ('toml', 'TOML', "Tom's Obvious Minimal Language"),
        ],
        default = 'toml',
    )
    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.filepath = f"templates.{self.format}"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

@bpyx.addon_setup.registree
class TemplatesImportOperator(TemplatesPersistenceOperator):
    bl_idname = f"{TemplatesPersistenceOperator.idname}_import"
    bl_label = "Import Templates"
    bl_description = "Import templates from TOML file"
    ui_icon = 'IMPORT'
    def execute(self, context: bpy.types.Context):
        try:
            with open(Path(bpy.path.abspath(self.filepath)), "rb") as file:
                try:
                    templates_dicts = tomllib.load(file).get("templates")
                except tomllib.TOMLDecodeError as exc:
                    self.report_error(f"TOML decoding error: {exc}")
                    return {'CANCELLED'}
            if not templates_dicts:
                self.report_info("TOML file is empty, nothing to import")
                return {'CANCELLED'}
            templates = props_templates_get_or_crt()
            for template_dict in templates_dicts:
                template = templates.add()
                template.from_dict(template_dict)
        except OSError as exc:
            self.report_invalid_input(f"Could not save the file due to an OS error: {exc}")
        except Exception as exc:
            self.report_exception_current(f'"{self.filepath}" {self.format}')
            return {'CANCELLED'}
        return {'FINISHED'}

@bpyx.addon_setup.registree
class TemplatesExportOperator(TemplatesPersistenceOperator):
    bl_idname = f"{TemplatesPersistenceOperator.idname}_export"
    bl_label = "Export Templates"
    bl_description = "Export templates to TOML file"
    ui_icon = 'EXPORT'
    def execute(self, context: bpy.types.Context):
        try:
            templates = props_templates_get_or_crt()
            with open(Path(bpy.path.abspath(self.filepath)), "w") as file:
                for template in templates:
                    file.write(f"[[templates]]\n{template.to_toml()}\n\n")
        except Exception as exc:
            self.report_exception_current(f'"{self.filepath}" {self.format}')
            return {'CANCELLED'}
        return {'FINISHED'}
