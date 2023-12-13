
import requests, qrcode, uuid
import json
import configparser

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
        payload = {"description": username, "max": self.max_lnurlp, "min": self.min_lnurlp, "comment_chars": 50, "username": username, "webhook_url": self.lnurlp_webhook + "/" + username }
        r = requests.post(
            url,
            data = json.dumps(payload),
            headers = {"Content-Type": "application/json",
                     "X-Api-Key": self.admin_key},
        )
        return r.json()
