discord-splash
==============

An API wrapper for Discord's slash commands.

|Maintainability| |Documentation Status|

Docs
~~~~~

|Documentation Status|

Docs are hosted on `ReadTheDocs.`_, and can be found in the ``docs`` directory.

**NOTE**
~~~~~~~~~

you are required to make the slash commands via the Discord API.
**Currently this is not possible via this API wrapper.**


Examples
~~~~~~~~~

More examples can be found in the ``examples`` directory

*Simple bot that responds with "hi"*

.. code:: python

   from discordSplash import Run
   import discordSplash

   @discordSplash.command(name='hello')
   async def hello(data):
       await data.respond(discordSplash.ReactionResponse("hi"))


   Run('TOKEN')

*Presence Example*

.. code:: python

   from discordSplash import Run, Presence
   import discordSplash

   x = Presence(text='testing', presenceType=discordSplash.PresenceType.Game)

   Run('TOKEN', x)

Voice Support
Installation
~~~~~~~~~~~~

Use ``pip install discordSplash``.

.. _ReadTheDocs.: https://discordsplash.readthedocs.io/en/latest/

.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/518e23ddf3bf0b0e065f/maintainability
   :target: https://codeclimate.com/github/Mineinjava/discord-splash/maintainability
.. |Documentation Status| image:: https://readthedocs.org/projects/discordsplash/badge/?version=latest
   :target: https://discordsplash.readthedocs.io/en/latest/?badge=latest