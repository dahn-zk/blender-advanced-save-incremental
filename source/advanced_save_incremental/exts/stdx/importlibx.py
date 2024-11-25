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

import importlib
import logging
import sys
from types import ModuleType
from typing import Iterable

logger = logging.getLogger(__name__)

def reload(root_module_name: str, excluded: Iterable[ModuleType] = None):
    """
    reload a module and its submodules.
    """
    for module_name, module in list(sys.modules.items()):
        if (
                module_name.startswith(root_module_name)  # submodule or root
                and len(module_name) > len(root_module_name)  # not root
                and (excluded is None or module not in excluded)
        ):
            importlib.reload(module)
            logger.debug(f"reloaded {module_name}")
