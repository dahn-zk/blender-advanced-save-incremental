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

from .importlibx import logger

class SafeCallMixIn():
    """
    min-in with `_safe_call` method to suppress repeated exeptions
    """
    #
    should_raise_exception_once = True
    #
    _had_exception = False
    def _safe_call(self, *args, **kwargs):
        raise NotImplementedError("_safe_call not implemented")
    def safe_call(self, *args, **kwargs):
        try:
            self._safe_call(*args, **kwargs)
        except Exception as exc:
            if not self.__class__._had_exception:
                self.__class__._had_exception = True
                logger.critical(exc, exc_info = exc)
                if self.should_raise_exception_once:
                    raise exc
