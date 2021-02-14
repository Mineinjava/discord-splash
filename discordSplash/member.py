class Member:
    """Represents a discord member. Used internally to parse interaction/member JSON data.

    :param json memberJson: JSON to parse into this class.

    TODO:

    - add a method to send a DM to the user

    - add an `avatar_url` property"""

    def __init__(self, memberJson):
        self.memberJson = memberJson

    @property
    def avatar(self):
        """
        :return: the member's avatar hash
        :rtype: str
        """
        return self.memberJson['avatar']

    @property
    def id(self):
        """
        :return: the user's id
        :rtype: int
        """
        return int(self.memberJson['id'])

    @property
    def username(self):
        """
        :return: the user's username
        :rtype: str
        """
        return self.memberJson['username']

    @property
    def discriminator(self):
        """
        .. Warning ::
            **CURRENTLY BROKEN**
            """
        return self.memberJson['id']
