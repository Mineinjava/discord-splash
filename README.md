# discord-splash
An API wrapper for Discord's slash commands.
 
### Docs:
coming soon™—use docstings for now.

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

x = Presence(text='testing', presenceType=5)

Run('TOKEN', x)
```
