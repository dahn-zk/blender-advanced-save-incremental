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
from collections.abc import Iterable
from os import PathLike

from .Template import Template

def templates_import(file_path: str | bytes | PathLike) -> list[Template]:
    with open(file_path, "rb") as file:
        templates_dict = tomllib.load(file)["templates"]
    templates = list(map(Template.from_dict, templates_dict))
    return templates

def templates_export(file_path: str | bytes | PathLike, templates: Iterable[Template]):
    with open(file_path, "w") as file:
        for template in templates:
            file.write(f"[[templates]]\n{template.to_toml()}\n\n")
