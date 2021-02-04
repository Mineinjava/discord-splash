from discordSlashCommands import Run, Presence
import discordSlashCommands
import requests
x = Presence(text='testing', presenceType=5)


@discordSlashCommands.command(name='say')
async def say(data):
    print('function called', data)
    url = f"https://discord.com/api/v8/interactions/{data['d']['id']}/{data['d']['token']}/callback"

    json = {
        "type": 3,
        "ephemeral": True,
        "data": {
            "flags": 64,
            "content": "Congrats on sending your command!"
        }
    }
    r = requests.post(url, json=json)
    print(r)

Run('TOKEN', x) #788160444341944402 or 806673167464136744