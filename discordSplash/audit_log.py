import discordSplash


class AuditLog:
    def __init__(self, jsondata):
        self.jsondata = jsondata

    @property
    def webhooks(self):
        """List of Webhooks found in the Audit Log
        :rtype: list
        :return: list of Webhook objects
        .. Error::
            You will receive a list of JSON data currently.
            """
        return self.jsondata['webhooks']

    @property
    def users(self):
        """Returns a list of all users found in the Audit log
        :return: list of discordSplash.member.Member objects
        :rtype: list"""
        listUsers = []
        for user in self.jsondata['users']:
            listUsers.append(discordSplash.member.Member(user))
        return listUsers

    @property
    def integrations(self):
        """
        Returns a list of all integrations found in the Audit Log.
        .. warning::
            May change from ``PartialIntegration`` to ``Integration``. See ``TODO`` in class PartialIntegration.
        :return: list of discordSplash.audit_log.PartialIntegration objects.
        :rtype: list
        """
        listIntegrations = []
        async for integration in self.jsondata['integrations']:
            listIntegrations.append(PartialIntegration(integration))
        return listIntegrations


class Entry:
    def __init__(self, jsondata):
        self.jsondata = jsondata


class PartialIntegration:
    def __init__(self, jsondata):
        """Partial integration object. Used mainly in Audit Logs
        TODO: make it a full integration object."""
        self.jsondata = jsondata

    @property
    def id(self):
        """ID of the integration
        :rtype: int"""
        return str(self.jsondata("id"))

    @property
    def name(self):
        """Name of the integration
        :rtype: str"""
        return self.jsondata("name")

    @property
    def type(self):
        """Type of the integration.
        :rtype: str"""
        return self.jsondata("type")

    @property
    def account(self):
        """integration account
        :return: Account of the integration
        :rtype: discordSplash.audit_log.Account"""
        return Account(self.jsondata("account"))


class Account:
    """
    Discord Account Object
    """

    def __init__(self, jsondata):
        self.jsondata = jsondata

    @property
    def name(self):
        """Name of the account.
        :rtype: str"""
        return self.jsondata("name")

    @property
    def id(self):
        """Id of the account.
        :rtype: int"""
        return int(self.jsondata("id"))
