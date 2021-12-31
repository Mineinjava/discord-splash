from dataclasses import dataclass
from datetime import datetime

from .abstractbaseclass import Object


@dataclass(init=False, eq=False)
class Channel(Object):
    """
    Represents a Discord channel

    Attributes
    ----------
    id : int
        ID of this channel
    
    type : int
        The type of channel
    
    guild_id : int
        ID of the guild
    
    position: int
        Sorting position of the channel
    
    permission_overwrites : array
        Permission overwrites for members and roles

    name : string
        Name of the channel

    topic : string
        Topic of the channel

    nsfw : bool
        Whether the channel is NSFW

    last_message_id : int
        ID of the most recent message sent in the channel
    
    bitrate : int
        Bitrate of the channel
    
    user_limit : int
        User limit of voice channel
    
    rate_limit_per_user : int
        Amount of seconds a user has to wait before sending another message
    
    recipients : array
        Recipients of the DM
    
    icon : string
        Icon hash
    
    owner_id : int
        ID of the creator of a group DM or thread

    application_id : int
        ID of the group DM creator if bot-created

    parent_id : int
        ID of the parent category

    last_pin_timestamp : timestamp
        When the most recent pin occured

    rtc_region : string
        Voice region ID for voice channel 
    
    video_quality_mode : int
        Camera video quality mode of the voice channel
    
    message_count : int
        Approximate count of messages in a thread
    
    member_count : int
        Approximate count of users in a thread
    
    thread_metadata : thread_metada
        Thread specific fields
    
    member : thread_member
        Thread member object for the current user
    
    default_auto_archive_duration : int
        Default duration for newly created threads
    
    permissions : string
        Computed permissions for the invoking user in the channel
    """

    def __init__(self, jsonData: dict):
        self.channelData = jsonData
        super.__init__(jsonData.get("id"))
        # Channel data variables
        self.id = int(self.channelData.get("id"))
        self.type = self.channelData.get("type")
        self.guild_id = int(self.channelData.get("guild_id?"))
        self.position = self.channelData.get("position?")
        self.permission_overwrites = self.channelData.get(
            "permission_overwrites?")  # TODO: Add an Overwrite object - https://discord.com/developers/docs/resources/channel#overwrite-object
        self.name = self.channelData.get("name?")
        self.topic = self.channelData.get("topic?")
        self.nsfw = self.channelData.get("nsfw?")
        self.last_message_id = int(self.channelData.get("last_message_id?"))
        self.bitrate = self.channelData.get("bitrate?")
        self.user_limit = self.channelData.get("user_limit?")
        self.rate_limit_per_user = self.channelData.get("rate_limit_per_user?")
        self.recipients = self.channelData.get("recipients?")
        self.icon = self.channelData.get("icon?")
        self.owner_id = int(self.channelData.get("owner_id?"))
        self.application_id = int(self.channelData.get("application_id?"))
        self.parent_id = int(self.channelData.get("parent_id?"))
        self.last_pin_timestamp = datetime.fromisoformat(self.channelData.get("last_pin_timestamp?"))
        self.rtc_region = self.channelData.get("rtc_region?")
        self.video_quality_mode = self.channelData.get("video_quality_mode?")
        self.message_count = self.channelData.get("message_count")
        self.member_count = self.channelData.get("member_count?")
        self.thread_metadate = self.channelData.get(
            "thread_metadata?")  # TODO: Add a Thread Metadata object - https://discord.com/developers/docs/resources/channel#thread-metadata-object
        self.member = self.channelData.get(
            "member?")  # TODO: Add a Thread Member object - https://discord.com/developers/docs/resources/channel#thread-member-object
        self.default_auto_archive_duration = self.channelData.get("default_auto_archive_duration?")
        self.permissions = self.channelData.get("permissions?")
