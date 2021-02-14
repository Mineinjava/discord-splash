from discordSplash import Run, Presence
import discordSplash
import requests
x = Presence(text='testing', presenceType=5)


@discordSplash.command(name='say')
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

Run('TOKEN', x) 
