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

from collections.abc import Iterator
from typing import Generic
from typing import TypeVar

import bpy

_T = TypeVar("_T")

class bpy_prop_collection_idprop(Generic[_T], bpy.types.bpy_prop_collection):
    """
    for type hints. there is no way this should be an internal Blender type.
    otherwise how are scripters supposed to know that Collection properties
    are mutable? which they crearly meant to be. good luck finding this in
    the Blender documentation as of 4.2.
    """
    def add(self) -> _T:
        pass
    def remove(self, index: int) -> None:
        pass
    def move(self, src_index: int, dst_index: int) -> None:
        pass
    def clear(self) -> None:
        pass
    def __len__(self) -> int:
        pass
    def __iter__(self) -> Iterator[_T]:
        pass

PropCollection = bpy_prop_collection_idprop  # a shorter alias
