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


class BaseSplashException(Exception):
    """exception that all exceptions in this module inherit from"""
    pass


class BaseSplashWarning(RuntimeWarning):
    """warning that all warnings in this module inherit from
    used when we do not want to stop execution of the program"""
    pass


class HTTPWarning(BaseSplashWarning):
    """Warning when something goes wrong with HTTP"""
    pass


class BadRequest(HTTPWarning):
    """The request was improperly formatted, or the server couldn't understand it.
    **This Shouldn't Happen** if this is raised, please report a bug."""
    pass


class Unauthorized(HTTPWarning):
    """The Authorization header was missing or invalid."""
    pass


class Forbidden(HTTPWarning):
    """The ``Authorization`` token you passed did not have permission to the resource."""
    pass


class NotFound(HTTPWarning):
    """The resource at the location specified doesn't exist."""
    pass


class MethodNotAllowed(HTTPWarning):
    """The HTTP method used is not valid for the location specified.
     **This Shouldn't Happen** if this is raised, please report a bug."""
    pass


class TooManyRequests(HTTPWarning):
    """raised when receiving a 429 response from the api.
    **this shouldn't happen.**"""
    pass


HTTPexceptionStatusPairing = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    429: TooManyRequests
}
