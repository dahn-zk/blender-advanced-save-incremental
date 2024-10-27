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

from . import config

logger = logging.getLogger(__name__)
if config.log: logger.setLevel(logging.DEBUG)

if config.dev:
    def _dev_reload():
        try:
            stdx.modules_sreload(__package__)
        except NameError:
            pass  # going to fail for the first time and it's okay
        except Exception as exc:
            logger.critical(exc, exc_info = exc)
    _dev_reload()

from . import stdx
from . import bpyx
from . import MainPanel

register, unregister = bpyx.addon_setup.registry_get()

if config.log: logger.debug(f"package loaded: {__package__}")
