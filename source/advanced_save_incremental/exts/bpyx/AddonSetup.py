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

"""
common prefs code for Blender add-ons. usage:

.. code-block:: python

    # a class to register/unregister: custom property, UI class, etc
    @addon_setup.registree
    class Prop(bpy.types.PropertyGroup):
        pass

    # custom pointer property on native data-block
    @bpyx.addon_setup.registree
    @addon_setup.custom_property_pointer(Prop, "my_prop")
    class MyProp(bpy.types.PropertyGroup):
        pass

    # handler
    @addon_setup.handler(bpy.app.handlers.load_post)
    def load_post():
        pass

    # timer
    @addon_setup.timer
    def timer():
        pass

    register, unregister = addon_setup.registry_get()

`addon_setup` is a module variable. be careful when reloading the module.
"""

import inspect
import logging
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Callable
from typing import TypeVar

import bpy

logger = logging.getLogger(__name__)

_bpy_struct_T = TypeVar('_bpy_struct_T', bound = bpy.types.bpy_struct)

@dataclass
class AddonSetup:
    """ common generic registration/unregistration code """

    # classes https://docs.blender.org/api/4.2/info_overview.html#module-registration
    registry: list[type] = field(default_factory = list)
    def registree(self, cls: type[_bpy_struct_T]):
        """ append *cls* to the list of types to register """
        if cls:
            self.registry.append(cls)
        return cls

    # handlers https://docs.blender.org/api/4.2/bpy.app.handlers.html
    # [handlers list, function]
    handlers_defs: list[tuple[list, Callable]] = field(default_factory = list)
    def handler(self, handlers_list: list):
        """ get a function to append a function to the *handlers_list* """
        def append(func: Callable):
            self.handlers_defs.append((handlers_list, func))
            return func
        return append

    # props https://docs.blender.org/api/4.2/bpy.props.html
    # [class, key, prop]
    custom_properties_defs: list[tuple[type, str, Any]] = field(default_factory = list)
    def custom_property_pointer(self, target_cls: type, attr_name: str):
        """
        get a function to append custom ``PointerProperty`` to the list
        of attributes to set on `target_cls`
        """
        def append(cls: type[bpy.types.bpy_struct]):
            self.custom_properties_defs.append((
                target_cls,
                attr_name,
                bpy.props.PointerProperty(type = cls),
            ))
            return cls
        return append

    # timers https://docs.blender.org/api/4.2/bpy.app.timers.html
    Timer = Callable[[], float | None]
    timers_defs: list[tuple[Timer, dict[str, Any]]] = field(default_factory = list)
    def timer(self, **kwags):
        def append(func: AddonSetup.Timer):
            self.timers_defs.append((func, kwags))
            return func
        return append

    def register(self,
            should_force_append_handlers = False,
            should_overwrite_attrs = False,
    ):
        """ graceful registration with error handling """
        logger.debug("registration started")
        for c in self.registry:
            try:
                bpy.utils.register_class(c)
                logger.debug(f"registered: {c}")
            except Exception as exc:
                source_path = Path(inspect.getsourcefile(c))
                logger.error((
                    "class registering failed. see the details below.\n"
                    f"class: {c}\n"
                    f"location: File \"{source_path}\""
                ), exc_info = exc)
        for h, f in self.handlers_defs:
            if not f in h or should_force_append_handlers:
                h.append(f)
                logger.debug(f"appended handler: {f}")
            else:
                logger.warning(
                    f"{f} is already in target handlers list. "
                    f"use 'should_force_add_handlers' if you intend to add duplicates.")
        for t, k, v in self.custom_properties_defs:
            if not hasattr(t, k) or should_overwrite_attrs:
                setattr(t, k, v)
                logger.debug(f"defined custom property: {t.__name__}.{k}")
            else:
                logger.warning(
                    f"{t} already has attribute '{k}'. "
                    f"use 'should_overwrite_attrs' if you intend to overwrite.")
        for f, kw in self.timers_defs:
            bpy.app.timers.register(f, **kw)
        logger.debug("registration finished")

    def unregister(self):
        """ graceful unregistration """
        logger.debug(f"unregisterion started")
        for c in reversed(self.registry):
            try:
                bpy.utils.unregister_class(c)
                logger.debug(f"unregistered: {c}")
            except Exception as exc:
                source_path = Path(inspect.getsourcefile(c))
                logger.error((
                    "class unregistering failed. see the details below.\n"
                    f"class: {c}\n"
                    f"location: File \"{source_path}\""
                ), exc_info = exc)
        for h, f in reversed(self.handlers_defs):
            try:
                h.remove(f)
                logger.debug(f"removed handler: {f}")
            except:
                pass  # ¯\_(ツ)_/¯
        for t, k, v in reversed(self.custom_properties_defs):
            try:
                delattr(t, k)
                logger.debug(f"deleted custom property: {t.__name__}.{k}")
            except:
                pass  # ¯\_(ツ)_/¯
        for f, _ in reversed(self.timers_defs):
            try:
                bpy.app.timers.unregister(f)
            except:
                pass  # ¯\_(ツ)_/¯
            logger.debug(f"unregistered timer: {f}")
        logger.debug("unregistration finished")

    def registry_get(self):
        return self.register, self.unregister

addon_setup: AddonSetup = AddonSetup()
