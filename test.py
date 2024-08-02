import requests

sl = {
    "type": 1,
    "date": "2020-11-03T11:49:32+0700",
    "currency": 1,
    "lang": "rus",
    "from_location": {
        "code": 270
    },
    "to_location": {
        "code": 44
    },
    "packages": [
        {
            "height": 10,
            "length": 10,
            "weight": 4000,
            "width": 10
        }
    ]
}
ans = requests.post("https://api.edu.cdek.ru/v2/calculator/tarifflist", json=sl).json()
print(ans)