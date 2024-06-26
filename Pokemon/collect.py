import requests
import json
import os
import datetime


class Collector:

    def __init__(self, url):
        self.url = url
        self.instance = url.strip("/").split("/")[-1]

    def get_endpoint(self, **kwargs):
        resp = requests.get(self.url, params=kwargs)
        return resp

    def save_data(self, data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        data['ingestion_time'] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        filename = f"/{self.instance}/{now}.json"
        with open(filename, "w") as open_file:
            json.dump(data, open_file)

    def get_and_save(self, **kwargs):
        resp = self.get_endpoint(**kwargs)
        if resp.status_code == 200:
            data = resp.json()
            self.save_data(data)
            return data
        else:
            return {}


url = 'https://pokeapi.co/api/v2/pokemon/'
collector = Collector(url)
collector.get_and_save()
