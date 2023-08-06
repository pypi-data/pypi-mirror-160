import requests
from config import username, password

headers = {'accept': 'application/json'}

def login():
    with requests.Session() as s:
        resp = s.post('http://127.0.0.1:5000/login', headers = headers, json={"username": username, "password": password})
        if resp.status_code != 200:
            return resp.json()
        headers.update(resp.json())
        #r = s.get("http://127.0.0.1:5000/message/0", headers = headers)
        #print(r.json())
        r = s.get("http://127.0.0.1:5000/announcements", headers=headers)
        print(r.json())

l = login()
print(l)