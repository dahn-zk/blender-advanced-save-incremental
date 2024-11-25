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

""" some values that should not or could not be in the add-on preferences """

import os
import pathlib
import tomllib
from urllib.parse import urljoin

log = os.environ.get("log", False)
""" to enable debug logging. """

dev = os.environ.get("dev", False)
""" to enable development/hacking features. """

addon_package = __package__.rpartition('.')[0]

addon_directory = pathlib.Path(globals().get("__file__", "./_")).absolute().parent.parent

with open(addon_directory / "blender_manifest.toml", "rb") as f:
    addon_manifest = tomllib.load(f)

addon_name = addon_manifest.get("name")

addon_qname = f"\"{addon_name}\""

addon_version = addon_manifest.get("version")

addon_url = addon_manifest.get("website")

addon_readme_url = urljoin(addon_url, f"blob/{addon_version}/README.md")

addon_key = addon_directory.stem
