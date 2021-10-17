@dataclass(init=False, eq=False)
class Presence:
    """Presence data used when connecting to Gateway

    Parameters
    ----------

    presenceType : Optional[discordSplash.enums.ActivityType]
        Type of presence to use.

    text : str
        Text of status to use.

    Hint
    ----
    ``x = Presence('a game', discordSplash.PresenceType.Game)``

    Warning
    -------
    Streaming URL's currently do not work

    Custom emojis have not been implemented in this API wrapper

    Attributes
    ----------
    type
    text : str
        Activity Text


        """

    def __init__(self, text: str, presenceType: enums.ActivityType = enums.ActivityType.Game):
        self.type_ = presenceType
        self.text = text

    @property
    def type(self):
        """Returns the type of the activity.

        Returns
        -------
        int 
            Integer from 1-5. 

            taken from `discordSplash.enums.ActivityType` class.
        """

        return self.type_.value