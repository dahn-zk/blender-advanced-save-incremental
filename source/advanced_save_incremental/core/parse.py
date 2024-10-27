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

import logging
import re

from .StemParts import StemParts
from .Template import Template
from .Version import Version
from .VersionTemplate import VersionTemplate

logger = logging.getLogger(__name__)

def parse_prefix(root: str, template: Template):
    root_len_old = len(root)
    root = root.removeprefix(template.prefix)
    prefix = template.prefix if len(root) < root_len_old else ""
    return root, prefix
def parse_suffix(root: str, template: Template):
    root_len_old = len(root)
    root = root.removesuffix(template.suffix)
    suffix = template.suffix if len(root) < root_len_old else ""
    return root, suffix
def parse_version(stem: str, version_template: VersionTemplate):
    if version_template.width <= 0:
        version_part_pattern = r"(\d+)"
    else:
        version_part_pattern = r"(\d{" + str(version_template.width) + ",})"
    version_parts_patterns = (
            [version_part_pattern] +
            [f"{version_part_pattern}"] * (version_template.count - 1))
    version_pattern = (
            f"({re.escape(version_template.separator)})"
            .join(version_parts_patterns) + "$")
    logger.debug(f"{version_pattern=}")
    version_match = re.search(version_pattern, stem)
    logger.debug(f"{version_match=}")
    if version_match:
        version_groups = version_match.groups()
        logger.debug(f"{version_groups=}")
        version_parts_strs = version_groups[::2]
        version_template.width = min([len(e) for e in version_parts_strs])
        version_parts = [int(e) for e in version_parts_strs if e.isnumeric()]
        root = stem.removesuffix("".join(version_groups))
    else:
        version_parts = list(VersionTemplate.config.default)
        root = stem
    return root, Version(version_parts, version_template)
def parse(stem: str, template: Template) -> StemParts:
    """
    given a file name stem extract root and version data

    for example, given the stem "forest_2-v1.12", prefix "pre_", suffix "-v",
    separator ".", width 1 and count 2, the result would be: ::

        StemParts(
            prefix = "",
            root = "forest_2",
            suffix = "-v",
            version = Version([1, 12]),
            template = VersionTemplate(
                prefix = "pre_",
                suffix = "-v",
                separator = ".",
                width = 1,
                count = 2,
            )
        )
    """
    root, version = parse_version(stem, template.version)
    root, prefix = parse_prefix(root, template)
    root, suffix = parse_suffix(root, template)
    return StemParts(prefix, root, suffix, version)
