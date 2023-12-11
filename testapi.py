#!/usr/bin/python3
# script for post or get data to an api endpoint

import requests
import json
import sys

(user,payment_hash,amount)=(sys.argv[1],sys.argv[2],sys.argv[3])


def test(user,payment_hash,amount):
    url="https://apidev.sats.contact/v1/lnurlp/webhook/" + user
    payload={
            'payment_hash': payment_hash,
            'payment_request': 'lnbc100n1pjk6eXXXX', 'amount': amount,
            'comment': None, 'lnurlp': 'o2GqNt', 'body': ''
    }
    r = requests.post(
        url,
        data = json.dumps(payload),
        headers = {"Content-Type": "application/json"},
    )
    return r



print(test(user,payment_hash,amount))
