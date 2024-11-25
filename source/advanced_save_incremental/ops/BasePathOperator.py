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
import textwrap
from pathlib import Path

from .BaseOperator import BaseOperator

logger = logging.getLogger(__name__)

class BasePathOperator(BaseOperator):
    path: Path
    def path_create_directory(self):
        try:
            self.path.mkdir(parents = True, exist_ok = True)
        except OSError as exc:
            self.report_invalid_input(textwrap.dedent(f"""\
                    Could not create the directory due to an OS error: {exc}
                    Directory: {self.path}
                    Make sure the path is valid, you have the access, disk space, etc.
                    """))
            logger.error(f"could not create directory at {self.path}\n", exc_info = exc)
