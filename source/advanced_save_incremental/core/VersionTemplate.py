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

@dataclass
class VersionTemplate:
    separator: str = "."
    count: int = 3
    width: int = 1
    class config:
        parts = ["Major", "Minor", "Patch"]  # à la semver
        """ 
        names of version elements.
        also defines maximum number of version elements.
        """
        width_max = 3
        """ maximum base width of a version element. """
        default = [0]
        """ 
        default version value as a of integers to know from where to start counting,
        usually from 0, but sometimes from 1.
        """
    def parts_names_get(self):
        return VersionTemplate.config.parts[:self.count]
    @staticmethod
    def from_dict(d: dict | None):
        version_template = VersionTemplate()
        if d is not None:
            version_template.separator = d.get("separator", version_template.separator)
            version_template.count = d.get("count", version_template.count)
            version_template.width = d.get("width", version_template.width)
        return version_template
