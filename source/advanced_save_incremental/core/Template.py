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

from dataclasses import dataclass

from .VersionTemplate import VersionTemplate
from ..exts.stdx.dataclassesx import DataclassFromDictMixIn

@dataclass
class Template(DataclassFromDictMixIn):
    name: str = "Unnamed Template"
    prefix: str | None = None
    suffix: str | None = None
    version: VersionTemplate | None = None
    def to_toml(template) -> str:
        lines = [f'name = "{template.name}"']
        if template.prefix is not None: lines.append(f'prefix = "{template.prefix}"')
        if template.suffix is not None: lines.append(f'suffix = "{template.suffix}"')
        if template.version is not None:
            lines.append(f'version.separator = "{template.version.separator}"')
            lines.append(f'version.count = {template.version.count}')
            lines.append(f'version.width = {template.version.width}')
        return '\n'.join(lines)
