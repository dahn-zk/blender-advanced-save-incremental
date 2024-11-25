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

Layout = bpy.types.UILayout

def draw_opening_arrow(layout: Layout, data, key: str, **kwargs):
    val = getattr(data, key, None)
    kwargs.setdefault("icon", 'DOWNARROW_HLT' if val else 'RIGHTARROW')
    kwargs.setdefault("text", "")
    kwargs.setdefault("emboss", False)
    layout.prop(data, key, **kwargs)

def draw_op_wm_url_open(layout: Layout, url: str, **kwargs):
    kwargs.setdefault("text", "")
    kwargs.setdefault("icon", 'URL')
    op = layout.operator("wm.url_open", **kwargs)
    op["url"] = url

def draw_op_preferences_addon_show(layout: Layout, module: str, **kwargs):
    kwargs.setdefault("text", "")
    kwargs.setdefault("icon", 'PREFERENCES')
    op = layout.operator("preferences.addon_show", **kwargs)
    op["module"] = module
