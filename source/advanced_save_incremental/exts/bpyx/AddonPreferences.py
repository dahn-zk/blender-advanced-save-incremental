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

from typing import Self

import bpy

class AddonPreferences(bpy.types.AddonPreferences):
    """
    base class for addon preferences
    """
    # https://docs.blender.org/api/4.2/bpy.types.AddonPreferences.html
    # https://docs.blender.org/manual/en/4.2/advanced/extensions/addons.html#user-preferences-and-package
    # bl_idname = __package__
    @classmethod
    def instance_get(cls) -> Self:
        return bpy.context.preferences.addons[cls.bl_idname].preferences
