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

"""
Miscellaneous utilities used by discordSplash
"""

import collections


def flatten(d: collections.MutableMapping, parent_key: str = '', sep: str = '_') -> dict:
    """
    flatten a dict

    credit goes to https://stackoverflow.com/a/6027615/13224997

    Parameters
    ----------
    d : dict
        dictionary to be flattened

    parent_key : str
        used internally for appending to a dict

    sep : str
        separating character in the flattened dict keys

    Returns
    -------
    dict
        the flattened dict.

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
