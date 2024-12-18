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

from ..exts.stdx import DataclassFromDictMixIn

@dataclass
class VersionTemplate(DataclassFromDictMixIn):
    separator: str = "."
    count: int = 3
    width: int = 1
    #
    class config:
        parts = ["Major", "Minor", "Patch"]
        width_max = 3
    #
    @staticmethod
    def part_get(idx: int):
        return VersionTemplate.config.parts[idx]
