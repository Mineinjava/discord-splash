from discordSplash import Run, Presence
import discordSplash
x = Presence(
    text='testing',
    presenceType=discordSplash.PresenceType.Competing)  # set the presence


@discordSplash.command(name='say')
async def say(data):
    # set arg1 to the value of the first argument
    arg1 = data.options[0]['value']
    await data.respond(arg1)  # respond to the command

Run('TOKEN', x)
