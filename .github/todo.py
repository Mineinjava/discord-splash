import sys
import re
import requests
github_token = sys.argv[1]
github_repo = sys.argv[2]
headers = {"authorization": f"Bearer {github_token}", 'content-type': 'application/json'}


py_files = ["__init__.py", "audit_log.py", "channel.py", "emoji.py", "guild.py", "invite.py", "main.py", "member.py", "opcodes.py", "template.py", "webhook.py"]
abs_py_files = []
data = ""
for file in py_files:
    with open(f"/home/runner/work/discord-splash/discordSplash/{file}", 'r') as r_file:
        data = data + r_file.read()


x = re.findall("TODO: .+ - .+", data)
todos = {}
for todo in x:
    new_x = todo.replace("TODO:", "")
    new_x_t = new_x.replace("|", "\n")
    a,b = new_x_t.split('-', 1)
    todos[a] = b

for todo_post in todos:
    body = {
        'title': todo_post,
        'body': todos[todo_post]
    }
    url = f"https://api.github.com/repos/{github_repo}/issues"
    x = requests.post(url=url, json=body, headers=headers)
    print(x)
