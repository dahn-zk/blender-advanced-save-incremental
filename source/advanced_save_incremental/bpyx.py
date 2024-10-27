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
miscellaneous reusable code not depending on a specific addon
"""

import inspect
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Generic
from typing import Self
from typing import TypeVar

import bpy

logger = logging.getLogger(__name__)

@dataclass
class AddonSetup:
    """ common generic registration/unregistration code """
    ### https://docs.blender.org/api/4.2/info_overview.html#module-registration
    registry: list[type] = field(default_factory = list)
    def registree(self, cls: type[bpy.types.bpy_struct]):
        """ append *cls* to the list of types to register """
        if cls:
            self.registry.append(cls)
        return cls
    ### https://docs.blender.org/api/4.2/bpy.app.handlers.html
    # [handlers list, function]
    handlers_defs: list[tuple[list, Callable]] = field(default_factory = list)
    def handler(self, handlers_list: list):
        """ get a function to append a function to the *handlers_list* """
        def append(func: Callable):
            self.handlers_defs.append((handlers_list, func))
            return func
        return append
    ### https://docs.blender.org/api/4.2/bpy.props.html
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
    ### https://docs.blender.org/api/4.2/bpy.app.timers.html
    Timer = Callable[[], float | None]
    timers_defs: list[tuple[Timer, dict[str, Any]]] = field(default_factory = list)
    def timer(self, **kwags):
        def append(func: Callable[[], float | None]):
            self.timers_defs.append((func, kwags))
            return func
        return append
    ###
    def register(self,
            should_force_append_handlers = False,
            should_overwrite_attrs = False,
    ):
        """ graceful registration with error handling """
        logger.debug(f"started registering package: {__package__}")
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
        logger.debug(f"finished registering package: {__package__}")
    def unregister(self):
        """ graceful unregistration """
        logger.debug(f"started unregistering package: {__package__}")
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
        logger.debug(f"finished unregistering package: {__package__}")
    ###
    def registry_get(self):
        return self.register, self.unregister

addon_setup: AddonSetup = AddonSetup()

class AddonPreferences(bpy.types.AddonPreferences):
    """ base class for addon preferences """
    # https://docs.blender.org/api/4.2/bpy.types.AddonPreferences.html
    # https://docs.blender.org/manual/en/4.2/advanced/extensions/addons.html#user-preferences-and-package
    bl_idname = __package__
    @classmethod
    def instance_get(cls) -> Self:
        return bpy.context.preferences.addons[__package__].preferences

_T = TypeVar("_T")

class bpy_prop_collection_idprop(Generic[_T], bpy.types.bpy_prop_collection):
    """
    for type hints. there is no way this should be an internal Blender type.
    otherwise how are scripters supposed to know that Collection properties
    are mutable? which they crearly meant to be. good luck finding this in
    the Blender documentation as of 4.2.
    """
    def add(self) -> _T:
        pass
    def remove(self, index: int) -> None:
        pass
    def move(self, src_index: int, dst_index: int) -> None:
        pass
    def clear(self) -> None:
        pass
    def __len__(self) -> int:
        pass
    def __iter__(self) -> Iterator[_T]:
        pass
# a shorter alias in Python style
PropCollection = bpy_prop_collection_idprop

def file_path_get():
    return Path(bpy.path.abspath(bpy.data.filepath))

def draw_opening_arrow(layout: bpy.types.UILayout, data, key: str, **kwargs):
    icon = 'DOWNARROW_HLT' if getattr(data, key) else 'RIGHTARROW'
    text = kwargs.pop("text", "")
    emboss = kwargs.pop("emboss", False)
    layout.prop(data, key, icon = icon, text = text, emboss = emboss, **kwargs)

def ops_names(root_key):
    ops: ModuleType = getattr(bpy.ops, root_key)
    return [f"bpy.ops.{root_key}." + op_name for op_name in dir(ops)]
