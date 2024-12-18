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

from .build import build_version_str
from .build import file_name_get
from .build import version_increment
from .FileSaveData import FileSaveData
from .parse import parse_stem
from .StemParts import StemParts
from .VersionParts import VersionParts
from .Template import Template
from .Version import Version
from .VersionTemplate import VersionTemplate

def tokenize_words_and_numbers(stem: str) -> tuple[str, ...]:
    return tuple(int(e) if e.isdigit() else e
        for e in re.split(r"(\d+)", stem))
