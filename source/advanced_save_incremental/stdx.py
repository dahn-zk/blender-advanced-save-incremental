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
import inspect
import logging
import sys
from types import ModuleType
from typing import Iterable

logger = logging.getLogger(__name__)

def kwargs_get(**kwargs):
    return kwargs

def module_rreload(module: ModuleType, memo: dict = None, depth = 0):
    module_name = module.__name__
    module_package = module.__package__
    log_indent = ' ' * (depth * 2)
    logger.debug(f"{log_indent}starting reloading {module_name}")
    if memo is None:
        memo = {}
    for attr_name, submodule in inspect.getmembers(module, inspect.ismodule):
        submodule_name = submodule.__name__
        if submodule_name.startswith(module_package):
            if submodule_name not in memo:
                submodule = module_rreload(submodule, memo, depth + 1)
                setattr(module, attr_name, submodule)
            else:
                logger.debug(f"{log_indent}already reloaded {submodule_name}")
    module = importlib.reload(module)
    memo[module_name] = module
    logger.debug(f"{log_indent} finished reloading {module_name}")
    return module

def modules_rreload(modules: Iterable[ModuleType], memo: dict = None, depth = 0):
    if memo is None:
        memo = {}
    for module in modules:
        module_rreload(module, memo, depth)

def modules_sreload(package_name: str, excluded: Iterable[ModuleType] = None):
    for module_name, module in list(sys.modules.items()):
        if (
                module_name.startswith(package_name)  # submodule or root
                and len(module_name) > len(package_name)  # not root
                and (excluded is None or module not in excluded)
        ):
            importlib.reload(module)
            logger.debug(f"reloaded {module_name}")

class SafeCaller():
    had_exception = False
    should_raise_exception_once = True
    def _safe_call(self, *args, **kwargs):
        raise NotImplementedError("_safe_call not implemented")
    def safe_call(self, *args, **kwargs):
        try:
            self._safe_call(*args, **kwargs)
        except Exception as exc:
            if not self.__class__.had_exception:
                self.__class__.had_exception = True
                logger.critical(exc, exc_info = exc)
                if self.should_raise_exception_once:
                    raise exc
