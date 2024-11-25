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

from typing import Any

from .FileSaveData import FileSaveData
from .Template import Template
from .Version import Version
from .VersionParts import VersionParts
from .VersionTemplate import VersionTemplate

def version_str(version: Version, fill: int = 0) -> str:
    separator = version.template.separator
    width = version.template.width
    count = version.template.count
    parts = version.parts
    return separator.join([str(e).rjust(width, str(fill))
        for e in (parts + [fill] * (count - len(parts)))])

def version_increment(
        parts: VersionParts,
        idx: int = -1,
        count = 1,
) -> VersionParts:
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
    if idx < 0: idx += len(parts)
    count = max(count, idx + 1)
    parts = list(map(int, parts)) + [0] * (count - len(parts))
    parts[idx] += 1
    for i in range(idx + 1, len(parts)):
        parts[i] = 0
    return parts

def build_version_str(
        template: VersionTemplate,
        parts: VersionParts,
        fill: Any = 0,
) -> str:
    if template is None:
        return ""
    else:
        parts = parts[:min(len(parts), template.count)]
        return template.separator.join([
            str(e).rjust(template.width, str(fill))
            for e in (parts + [fill] * (template.count - len(parts)))])

def file_name_get(
        template: Template,
        root: str,
        version_parts: VersionParts,
):
    prefix = template.prefix if template.prefix else ""
    suffix = template.suffix if template.suffix else ""
    version = build_version_str(template.version, version_parts)
    return f"{prefix}{root}{suffix}{version}.blend"

def files_save_datas_gen(
        template: Template,
        version_parts: VersionParts,
        root: str,
        phrase: str = "Save",
):
    # simple save
    yield FileSaveData(
        label = phrase,
        file_name = file_name_get(template, root, version_parts),
    )
    # incremental saves
    if template.version is not None:
        count = template.version.count
        for increment_idx in range(count):
            version_parts_inc = version_increment(version_parts, increment_idx, count)
            version_str = build_version_str(template.version, version_parts_inc)
            if count == 1:
                label = f"{phrase} Incremental: {version_str}"
            else:
                version_part_name = VersionTemplate.part_get(increment_idx)
                label = f"{phrase} Incremented {version_part_name}: {version_str}"
            yield FileSaveData(
                label = label,
                file_name = file_name_get(template, root, version_parts_inc),
            )
