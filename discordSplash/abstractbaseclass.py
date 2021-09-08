# Copyright (C) 2021-Present Mineinjava

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import datetime


class Object:
    """
    base ABC that all objects should inherit from

    .. Admonition:: Operations

        **x == y**

        checks if two objects are equal

        **x != y**

        checks if two objects are not equal

        **int(x)**

        returns the object's discord id

    Parameters
    ----------
    id : int
        id of the object.


    Attributes
    ----------
    id : int
        id of the object.

    timestamp : :class:`datetime.datetime`
        timestamp of when the object was created.
    """

    def __init__(self, id: int):
        self.id = id
        # bit of math that gets the timestamp
        epochts = (int(bin(id).replace("0b", ''), 2) >> 22) + 1420070400000
        self.timestamp = datetime.datetime.fromtimestamp(epochts)

    def __int__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id


class BaseChannel(Object):
    """
    base ABC that channels should inherit from

    .. Admonition:: Operations

        **x == y**

        checks if two objects are equal

        **x != y**

        checks if two objects are not equal

        **int(x)**

        returns the object's discord id
    """

    def __init__(self, json: dict):
        self.id = json.get('id')
        super().__init__(self.id)
