
class Channel:
    """
    Represents a Discord Channel Object.
    """
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        """
        x
        :return:
        :rtype:
        """
        try:
            return self.json['x']
        except KeyError:
            return None
