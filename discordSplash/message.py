from . import user
from dataclasses import dataclass

from datetime import datetime

@dataclass(init=False, eq=False)
class Message():
    """
    Represents a Discord message

    Attributes
    ----------
    id : int
        ID of the message

    channel_id : int
        ID of the channel the message was sent in
    
    guild_id : int
        ID of the guild the message was sent in    
    
    author : user
        Author of the message
    
    member : guild_member
        Partial guild member object

    content : str
        Content of the message

    timestamp : timestamp
        When the message was sent
    
    edited_timestamp: timestamp
        When the message was edited, none if not edited
    
    tts : bool
        Whether the message was a TTS message
    
    mention_everyone : bool
        Whether or not the message mentions @everyone
    
    mentions : array
        Users specifically mentioned in the message

    mention_roles : array
        Roles specifically mentioned in the message
    
    mention_channels : array
        Channels specificall mentioned in the message
    
    attachments : array
        Any attached files
    
    embeds : array
        Any embedded content
    
    reactions : array
        Reactions to the message
    
    nonce : int or string
        For validating a message was sent
    
    pinned : bool
        Whether the message is pinned
    
    webhook_id : int
        If the message is generated by a webhook, the webhook's ID

    type : int
        Type of message
    
    activity : message_activity
        Sent with Rich Presence related chat embeds
    
    application : application
        Sent with Rich Presence related chat embeds
    
    application_id : int
        The ID of an interaction's application
    
    message_reference : message_reference
        Data showing the soource of a crosspost
    
    flags : int
        Message flags as a bitfield
    
    referenced_message : message
        Message associated with message_reference
    
    interaction : message_interaction
        Sent if the message is a response to an Interaction
    
    thread : channel
        The thread that was started from this message. Include thread member object (NOT YET IMPLEMENTED)
    
    components : array
        Sent if the message contains components like buttons, or other interactive components
    
    sticker_items : array
        Sent if the message contains sticker item objects
    """
    def __init__(self, jsonData : dict):
        self.messageData = jsonData
        
        # Message data variables
        self.id                 = int(self.messageData.get("id"))
        self.channed_id         = int(self.messageData.get("channel_id"))
        self.guild_id           = int(self.messageData.get("guild_id?"))
        self.author             = user.User(self.messageData.get("author"))
        self.member             = self.messageData.get("member?")                                       # TODO: Add a Member object - https://discord.com/developers/docs/resources/guild#guild-member-object
        self.content            = self.messageData.get("content")
        self.timestamp          = datetime.fromisoformat(self.messageData.get("timestamp"))
        self.edited_timestamp   = datetime.fromisoformat(self.messageData.get("edited_timestamp"))
        self.tts                = self.messageData.get("tts")
        self.mention_everyone   = self.messageData.get("mention_everyone")
        self.mentions           = self.messageData.get("mentions")                                      
        self.mention_roles      = self.messageData.get("mention_roles")                                 # TODO: Add a Role object - https://discord.com/developers/docs/topics/permissions#role-object
        self.mention_channels   = self.messageData.get("mention_channels")                              # TODO: Add a Channel Mention object - https://discord.com/developers/docs/resources/channel#channel-mention-object
        self.attachments        = self.messageData.get("attachments")                                   # TODO: Add an Attachment object - https://discord.com/developers/docs/resources/channel#attachment-object
        self.embeds             = self.messageData.get("embeds")                                        # TODO: Add an Embed object - https://discord.com/developers/docs/resources/channel#embed-object
        self.reactions          = self.messageData.get("reactions?")                                    # TODO: Add a Reaction object - https://discord.com/developers/docs/resources/channel#reaction-object
        self.nonce              = self.messageData.get("nonce?")
        self.pinned             = self.messageData.get("pinned")
        self.webhook_id         = int(self.messageData.get("webhook_id?"))
        self.type               = self.messageData.get("type")
        self.activity           = self.messageData.get("activity?")                                     # TODO: Add a Message Activity oject - https://discord.com/developers/docs/resources/channel#message-object-message-activity-structure
        self.application        = self.messageData.get("application")                                   # TODO: Add an Application object - https://discord.com/developers/docs/resources/application#application-object
        self.application_id     = int(self.messageData.get("application_id?"))
        self.message_reference  = self.messageData.get("message_reference?")                            # TODO: Add a Message Reference object - https://discord.com/developers/docs/resources/channel#message-reference-object-message-reference-structure
        self.flags              = self.messageData.get("flags?")
        self.referenced_message = self.messageData.get("referenced_message?")
        self.interaction        = self.messageData.get("interaction?")                                  # TODO: Add a Message Interaction object - https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object-message-interaction-structure
        self.thread             = self.messageData.get("thread?")                                       
        self.components         = self.messageData.get("components?")
        self.sticker_items      = self.messageData.get("sticker_items?")                                # TODO: Add a Sticker Item object - https://discord.com/developers/docs/resources/sticker#sticker-item-object
