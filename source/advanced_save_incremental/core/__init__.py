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

""" core structures and functions not depending on the Blender API """

import re

from .parse import parse
from .StemParts import StemParts
from .Template import Template
from .Version import Version
from .VersionTemplate import VersionTemplate

def version_str(
        version: Version,
        fill: int = 0,
) -> str:
    separator = version.template.separator
    width = version.template.width
    count = version.template.count
    parts = version.parts
    return separator.join([str(e).rjust(width, str(fill))
        for e in (parts + [fill] * (count - len(parts)))])

def version_inc(
        version: Version,
        index: int = -1,
        count = 1,
) -> Version:
    """
    increment version element at index and reset all following elements to 0.
    if the index is larger than the size, then zeroes are appended.

    examples:

    * [1], index = 0 -> [2]
    * [1], index = 1 -> [1, 1]
    * [1, 2], index = 0 -> [2, 0]
    * [1, 2], index = 1 -> [1, 3]
    * [1], index = 2 -> [1, 0, 1]
    """
    parts = version.parts
    if index < 0: index += len(parts)
    count = max(count, index + 1)
    parts = list(map(int, parts)) + [0] * (count - len(parts))
    parts[index] += 1
    for i in range(index + 1, len(parts)):
        parts[i] = 0
    version.parts = parts
    return version

def tokenize_words_and_numbers(stem: str) -> tuple[str, ...]:
    return tuple(int(e) if e.isdigit() else e
        for e in re.split(r"(\d+)", stem))
