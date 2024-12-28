import os
import threading, json, numpy as np, random, requests, itertools
from rich import print
from time import sleep

config = {
    "webhook": "webhook gır",
    "importListFrom": "usernames.txt",
    "generateTo": "usernames.txt",
    "rotating": False,
    "proxy": "proxies.txt",
    "threads": 10, # hız bura 500 ustune cıkma
    "showTaken": True,
    "showAvailable": True,
    "license": "License Info"
}

def chunks(lst, n):
    return np.array_split(lst, n)

def webhook(user):
    embed_data = {
        "title": "Username Available!",
        "description": f"• **Username** : `{user} :>`\n [Join the Discord Server](https://discord.gg/1937)",
        "color": 65280,
        "footer": {
            "text": "developed by duckevils [>.<]",
            "icon_url": "https://cdn.discordapp.com/attachments/1138418027294109757/1316061055587323965/54e898f565e5b0637e921475726b841f.png?ex=6759acde&is=67585b5e&hm=e6e5e9aa90f1eb8df0a4638ec205df9ec5ab36f27a5d72140008e971e4c9172c&"
        }
    }
    data = {"content": None, "embeds": [embed_data], "attachments": []}
    headers = {"Content-Type": "application/json"}
    requests.post(config['webhook'], data=json.dumps(data), headers=headers)

def checker(lst):
    for i in lst:
        try:
            if config['rotating']:
                proxy = config['proxy']
            else:
                proxy = (random.choice(open("proxies.txt", 'r').readlines())).replace('\n', '')
            r = requests.post("https://discord.com/api/v9/unique-username/username-attempt-unauthed", proxies={"https": f"http://{proxy}"}, json={"username": i}, headers={"content-type": "application/json"})
            if r.status_code == 429:
                print('Rate-Limit')
            elif 'true' in r.text:
                print(f'User Not Available: [ [red]{i}[/red] ]') if config['showTaken'] else None
            elif 'false' in r.text:
                print(f'User is Available:  [ [green]{i}[/green] ]') if config['showAvailable'] else None
                webhook(i)
            else:
             pass
        except requests.exceptions.MissingSchema:
            pass
        sleep(1)

def handler():
    threads = []
    print("[yellow]1[/yellow] - List Check")
    print("[yellow]2[/yellow] - Generate List")
    
    choice = int(input('> '))
    
    if choice == 1:
        users = []
        for i in open(config['importListFrom'], 'r').read().splitlines():
            users.append(i)
        for i in chunks(users, config['threads']):
            t = threading.Thread(target=checker, args=(i,))
            t.start()
            threads.append(t)
            sleep(0.1)
        for t in threads:
            t.join()

    elif choice == 2:
        out = []
        sub_choice = int(input('User Length : '))
        with open(config['generateTo'], 'w') as file:
            for length in range(sub_choice, sub_choice + 1):
                for combination in map(''.join, itertools.product('abcdefghijklmnopqrstuvwxyz1234567890', repeat=length)):
                    file.write(combination + '\n')
        print('[[cyan]+[/cyan]] - Done Generating List.')

    elif choice == 6:
        exit()

handler()
