import requests

url = "https://face-detection6.p.rapidapi.com/img/face"

payload = {
    "url": "https://inferdo.com/img/face-1.jpg",
    "accuracy_boost": 2
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "f284b2710fmsh1231062717b4c86p13e920jsn84b32f9b724c",
    "X-RapidAPI-Host": "face-detection6.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
