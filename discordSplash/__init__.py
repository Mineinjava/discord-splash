"""
DiscordSplash
~~~~~~~~~~~~~

A wrapper for Discord's Interactions and Slash Commands

"""

__version__ = '1.0.0a0'
__author__ = 'Mineinjava'
__copyright__ = "Copyright © 2021-Present Mineinjava"
__license__ = "GNU GPLv3"

from .gateway import GatewayBot
from .enums import ActivityType, ApplicationCommandOptionType
from .presence import Activity, UpdatePresence
