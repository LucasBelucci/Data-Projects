import json
import requests
import pprint
import pandas as pd

base_url = "https://edhtop16.com/api/"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

data = {
    'standing': {'$lte': 16},
    # 'colorID': 'WUBRG',
    'tourney_filter': {
        'size': {'$gte': 32}
    }
}

entries = json.loads(requests.post(
    base_url + 'req', json=data, headers=headers).text)
pretty_json = json.dumps(entries, indent=4)
# print(pretty_json)

df = pd.DataFrame(entries)
# df.to_csv('Commanders_Top16.csv')


# Lista de commanders

commanders = json.loads(requests.get(
    base_url + 'get_commanders', headers=headers).text)

pretty_json = json.dumps(commanders, indent=4)

# print(pretty_json)

# pprint.pprint(commanders)

# df = pd.DataFrame(commanders)
# df.to_csv('Commanders.csv')


# Get tournaments of at least 50 entries played since 2023-01-14


data = {
    'size': {'$gte': 50},
    'dateCreated': {'$gte': 1673715600}
}
tourneys = json.loads(requests.post(
    base_url + 'list_tourneys', json=data, headers=headers).text)

tourneys_json = json.dumps(tourneys, indent=4)

df = pd.DataFrame(tourneys)
df.to_csv('Tournaments.csv')
