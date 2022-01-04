from dataclasses import dataclass
from datetime import datetime

from . import user
from .abstractbaseclass import Object

@dataclass(init=False, eq=False)
class Role(Object):
    def __init__(self, json):
        super().__init__(json.get('id'))
        self.json = json
        self.name = self.json.get("name")
        self.color = self.json.get("color") #TODO add color object
        self.is_hoisted = self.json.get("hoist")
        self.icon = self.json.get("icon") #TODO: ADD ICON OBJECT
        self.emoji = self.json.get("unicode_emoji")
        self.position = self.json.get("position")
        self.permissions = self.json.get("permissions") #TODO IMPLEMENT Permissions
        self.managed = self.json.get("managed")
        self.mentionable = self.json.get("mentionable")
        self.tags = self.json.get("tags") #TODO: ADD ROLE TAGS OBJECT


@dataclass(init=False, eq=False)
class Member(Object):
    """
    Represents a Discord Guild Member

    Attributes
    ----------
    user : user
        The user this member represents
    
    nick : string
        User's guild nickname
    
    roles : array
        Role object IDs
    
    joined_at : timestamp
        The time the user join the guild
    
    premium_since : timestamp
        The time the user began boosting the guild
    
    deaf : bool
        Whether the user is deafend in voice channels
    
    mute : bool
        Whether the user is muted in voice channels
    
    pending : bool
        Whether the user has completed Membership Screening
    
    permissions : string
        Total permissions of the member in the channel
    """

    def __init__(self, jsonData: dict):
        self.memberData = jsonData

        # Member data variables
        self.user = user.User(self.memberData.get("user"))
        self.nick = self.memberData.get("nick")
        self.roles = self.memberData.get("roles")
        self.joined_at = datetime.fromisoformat(self.memberData.get("joined_at"))
        self.premium_since = datetime.fromisoformat(self.memberData.get("premium_since"))
        self.deaf = self.memberData.get("deaf")
        self.mute = self.memberData.get("mute")
        self.pending = self.memberData.get("pending")
        self.permissions = self.memberData.get("permissions")

