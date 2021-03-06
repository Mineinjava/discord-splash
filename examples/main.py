from discordSplash import Run, Presence
import discordSplash
x = Presence(text='testing', presenceType=discordSplash.PresenceType.Competing)  # set the presence


@discordSplash.command(name='say')
async def say(data):
    arg1 = data.options[0]['value']  # set arg1 to the value of the first argument
    await data.respond(arg1)  # respond to the command

Run('TOKEN', x) 
