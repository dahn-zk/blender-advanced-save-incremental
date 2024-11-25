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

import re
from typing import Sequence

import bpy

from ..exts import bpyx
from .. import core
from ..ops.FileOpenOperator import FileOpenOperator
from ..props.FilePathProps import FilePathProps
from ..prefs.Preferences import Preferences

@bpyx.addon_setup.registree
class ASI_UL_files(bpy.types.UIList):
    # note that the class name must be this way (with _UL_ infix) as for blender 4.2
    # https://docs.blender.org/api/4.2/bpy.types.UIList.html
    #
    def draw_item(self,
            context: bpy.types.Context,
            layout: bpy.types.UILayout,
            data,
            item: FilePathProps,
            icon: int | None,
            active_data,
            active_property: str,
            index: int | None = 0,
            flt_flag: int | None = 0,
    ):
        row = layout.row(align = True)
        # an expanded appearance but with left-adjusted text would be best, but...
        # row.alignment = 'EXPAND'  # expands, but text is centered
        # row.alignment = 'CENTER'  # same thing in this context
        row.alignment = 'LEFT'  # does not expand, but better than centered
        op = FileOpenOperator.drawx(row,
            text = f"{item.stem}.blend", icon = 'FILE_BLEND',
            emboss = Preferences.instance_get().file_items_emboss_get())
        op.filepath = item.path
    #
    def filter_items(self,
            context: bpy.types.Context,
            list_data,
            property_identifier: str,
    ):
        # https://github.com/blender/blender/blob/v4.2.1/scripts/startup/bl_ui/__init__.py#L205
        items: Sequence[FilePathProps] = getattr(list_data, property_identifier)
        def sorting_key(p: tuple[int, FilePathProps]):
            value = p[1].stem_get().lower()
            if self.use_filter_sort_alpha:
                res = value
            else:
                res = core.tokenize_words_and_numbers(value)
            return res
        sorting = sorted(enumerate(items), key = sorting_key)
        filter_neworder = [0] * len(sorting)
        for newidx, (orgidx, _) in enumerate(sorting):
            filter_neworder[orgidx] = newidx
        filter_flags = [0] * len(items)
        for i, item in enumerate(items):
            item: FilePathProps
            if re.match(fr".*{self.filter_name}.*", item.stem_get(), re.IGNORECASE):
                filter_flags[i] |= self.bitflag_filter_item
        return filter_flags, filter_neworder
