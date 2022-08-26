import time

import requests

url = "http://192.168.255.20:32758/?tt"

payload = {}
headers = {}
while True:
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    time.sleep(0.1)
