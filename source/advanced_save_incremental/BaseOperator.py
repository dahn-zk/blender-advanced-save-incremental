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

import textwrap
import traceback
from typing import Self

import bpy

from .Globals import Globals

class BaseOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'INTERNAL'}
    #
    icon: str = None
    #
    @classmethod
    def draw_layout(cls, layout: bpy.types.UILayout, **kwargs) -> Self:
        if cls.icon is not None:
            kwargs["icon"] = cls.icon
        return layout.operator(cls.bl_idname, **kwargs)
    #
    def _sorry_exception_message(self, why: str = ""):
        """ :( """
        return textwrap.dedent(f"""\
            Sorry, an unhandled error occured in the add-on {Globals.addon_qname}.
            Please copy this message and report it to the add-on maintainer.
            {why}
            {traceback.format_exc()}""")
    #
    def report_info(self, message: str):
        self.report({"INFO"}, message)
    def report_warning(self, message: str):
        self.report({"WARNING"}, message)
    def report_error(self, message: str):
        self.report({"ERROR"}, message)
    def report_invalid_input(self, message: str):
        self.report({"ERROR_INVALID_INPUT"}, message)
    def report_exception_current(self, message = ""):
        self.report({"ERROR"}, self._sorry_exception_message(why = message))
