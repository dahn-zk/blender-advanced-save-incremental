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

import textwrap

from ..exts import bpyx
from ..prefs import config

def info_code_get(data) -> str:
    comment = textwrap.indent(
        textwrap.fill(
            f"This Text stores {config.addon_qname} add-on data in hidden "
            f"custom properties. It can be safely deleted if you do not use "
            f"this add-on in this Blender file."
            f"The code below is just informational for ease of debugging/hacking "
            f"if you need to."),
        "# ")
    code = "\n".join(
        [
            "",
            f"import {__package__} as asi",
            "",
            "# data",
            repr(data),
            "",
            "# operators",
        ] + bpyx.ops_names(config.addon_key) +
        [
            "",
            "# core logic",
            f"import {__package__}.core as asi_core"
        ]
    )
    return comment + "\n" + code
