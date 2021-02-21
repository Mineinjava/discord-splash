# discord-splash
An API wrapper for Discord's slash commands.

[![Maintainability](https://api.codeclimate.com/v1/badges/518e23ddf3bf0b0e065f/maintainability)](https://codeclimate.com/github/Mineinjava/discord-splash/maintainability) [![Documentation Status](https://readthedocs.org/projects/discordsplash/badge/?version=latest)](https://discordsplash.readthedocs.io/en/latest/?badge=latest) [![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=Mineinjava/discord-splash)](https://dependabot.com)

### Docs:
[![Documentation Status](https://readthedocs.org/projects/discordsplash/badge/?version=latest)](https://discordsplash.readthedocs.io/en/latest/?badge=latest)

Docs are hosted on [ReadTheDocs.](https://discordsplash.readthedocs.io/en/latest/)
### **NOTE:**
you are required to make the slash commands via the Discord API. ***Currently* this is not possible via this API wrapper.**
### Examples:
*Simple bot that responds with "hi"*
```python
from discordSplash import Run
import discordSplash

@discordSplash.command(name='hello')
async def hello(data):
    await data.respond(discordSplash.ReactionResponse("hi"))


Run('TOKEN')
```

*Presence Example*
```python
from discordSplash import Run, Presence
import discordSplash

x = Presence(text='testing', presenceType=discordSplash.PresenceType.Game)

Run('TOKEN', x)
```
### Installation
Use `pip install discordSplash`

