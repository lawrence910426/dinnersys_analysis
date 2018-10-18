import requests
import json
from encoding import remove_bom

class fetch_data:
    server_dns = "http://dinnersystem.ddns.net/"
    def __init__(self, account, pswd):
        self.cookie = self.login(account, pswd)

    def login(self ,account, pswd):
        link = self.server_dns + "dinnersys_beta/backend/backend.php?cmd=login&id=" + \
            account + "&password=" + pswd
        session = requests.Session()
        resp = session.get(link)
        resp_text = remove_bom(resp.text)
        try:
            js = json.loads(resp_text)
            valid_oper = dict()
            for item in js["valid_oper"]:
                valid_oper[list(item.keys())[0]] = True
            if(not valid_oper["select_other"]):
                raise Exception("Not enough prev")
        except TypeError:
            raise Exception("Not enough prev")
        except Exception:
            raise Exception("Invalid id/pswd")
        return session.cookies.get_dict()

    def get_orders(self ,start ,end):
        link = self.server_dns + "dinnersys_beta/backend/backend.php?cmd=select_other&esti_start=" + \
            start + "&esti_end=" + end
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


