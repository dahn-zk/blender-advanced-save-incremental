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

from typing import get_args
from typing import get_origin
from types import UnionType
from dataclasses import dataclass
from dataclasses import fields

@dataclass
class DataclassFromDictMixIn:
    def __init__(self, **kwargs):
        pass
    @classmethod
    def from_dict(cls, d: dict | None):
        if d is None:
            return cls()
        else:
            args = {}
            for f in fields(cls):
                if f.name in d:
                    if get_origin(f.type) is UnionType:
                        for t in get_args(f.type):
                            if issubclass(t, DataclassFromDictMixIn):
                                args[f.name] = t.from_dict(d[f.name])
                                break
                        else:
                            args[f.name] = d[f.name]
                    elif issubclass(f.type, DataclassFromDictMixIn):
                        args[f.name] = f.type.from_dict(d[f.name])
                    else:
                        args[f.name] = d[f.name]
            return cls(**args)
