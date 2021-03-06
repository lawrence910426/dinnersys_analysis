import requests
import json
from internet_data.encoding import remove_bom
from data_structure.order import order
import pickle
import hashlib
import time
import json


class fetch_data:
    server_dns = "http://dinnersystem.com/"

    def __init__(self):
        self.cookie = self.login()

    def login(self):
        link = self.server_dns + "dinnersys_beta/backend/backend.php?cmd=login&id=dinnersys&password=sc2rjurrru&device_id=analysiser"
        
        session = requests.Session()
        resp = session.get(link)
        resp_text = remove_bom(resp.text)

        return session.cookies.get_dict()

    def get_orders(self):
        link = self.server_dns + "dinnersys_beta/backend/backend.php?cmd=select_other&history=true"
        f = requests.get(link, cookies=self.cookie)
        resp = remove_bom(f.text)
        ret = json.loads(resp)
        return ret

    def get_dish(self):
        link = self.server_dns + "dinnersys_beta/backend/backend.php?cmd=show_dish"
        f = requests.get(link, cookies=self.cookie)
        resp = remove_bom(f.text)
        ret = json.loads(resp)
        return ret

    @staticmethod
    def download(route):
        fetcher = fetch_data()
        data = order.get_order(fetcher)

        with open(route, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def load(route, start, end):
        with open(route, 'rb') as f:
            data = pickle.load(f)
            return order.select_order(data, start, end)

    @staticmethod
    def get(data, start, end):
        return order.select_order(data, start, end)
