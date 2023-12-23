
import requests, qrcode, uuid
import json
import configparser
import re
import random,string,qrcode

settings = configparser.ConfigParser()
settings.read('settings.ini')


class Lnurlp:

    def __init__(self):
        self.wallet_id =  settings['lnbits']['wallet_id']
        self.admin_key = settings['lnbits']['admin_key']
        self.lnbits_server = settings['lnbits']['lnbits_server']
        self.lnurlp_webhook = settings['lnbits']['lnurlp_webhook']
        self.min_lnurlp = settings['lnbits']['min_lnurlp']
        self.max_lnurlp = settings['lnbits']['max_lnurlp']
        self.success_text = settings['lnbits']['success_text']


    def create_lnurlp(self, username):
        # what is returned
        # {'id': 'o2GqNt', 'wallet': '60b2c788XXXXX', 'description': 'Lnurlp for userusertest',
        # 'min': 10.0, 'served_meta': 0, 'served_pr': 0, 'username': 'usertest', 'zaps': False, 'domain': None,
        # 'webhook_url': 'https://yourhost/v1/lnurlp/webhook/usertest', 'webhook_headers': None, 'webhook_body': None,
        # 'success_text': None, 'success_url': None, 'currency': None, 'comment_chars': 50, 'max': 10000.0,
        # 'fiat_base_multiplier': 100, 'lnurl': 'LNURL1DP68GURN8GHJ7XXXXXXX'}
        # or
        # {'detail': 'Username already exists. Try a different one.'}
        url     = f"{self.lnbits_server}/lnurlp/api/v1/links"
        payload = {"description": username, "max": self.max_lnurlp,
                   "success_text": self.success_text,
                   "min": self.min_lnurlp,
                   "comment_chars": 50,
                   "username": username,
                   "webhook_url": self.lnurlp_webhook + "/" + username }
        r = requests.post(
            url,
            data = json.dumps(payload),
            headers = {"Content-Type": "application/json",
                     "X-Api-Key": self.admin_key},
        )
        return r.json()



    def pay_invoice(self, invoice):
        url = f"{self.lnbits_server}/api/v1/payments"
        payload = {"out": True, "bolt11": invoice}
        r = requests.post(
            url,
            data = json.dumps(payload),
            headers = {"Content-Type": "application/json",
                      "X-Api-Key": self.admin_key},
        )
        return r.json()


    def get_balance(self):
        # {'id': 'xxxx', 'name': '200000000 (@massmux)', 'balance': 5070350}
        # {'name': '200000000 (@massmux)', 'balance': 5070350}
        url = f"{self.lnbits_server}/api/v1/wallet"
        result = {}
        try:
            r = requests.get(
                url,
                headers={"Content-Type": "application/json",
                         "X-Api-Key": self.admin_key},
            )
        except:
            return {}
        return r.json()


class CorrectUsername:
    def __init__(self,oString):
        self.oString=oString

    def get_transformed(self):
        transformed = re.sub("[^0-9a-z]", "", self.oString.lower())[:15]
        if len(transformed)<3:
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(10))
            transformed = result_str
        return transformed

