#!/usr/bin/python3


from flask_restful import Api
from flask_restful import Resource, reqparse
import requests

from flask import Flask, jsonify, request, redirect

from db import *
import time


app = Flask(__name__)
api = Api(app)



@app.route('/v1/lnurlp/webhook/<username>', methods=['POST'])
def lnurlp_webhook(username):
    # what is returned
    # {'payment_hash': '87a15cb2c3c4a698885d2ffbc3d7997923a72695bb87e9f30acb81e5bf54fd93', 
    #'payment_request': 'lnbc100n1pjk6eXXXX', 'amount': 10000, 
    #'comment': None, 'lnurlp': 'o2GqNt', 'body': ''}
    content = request.get_json(silent=True)
    print(content)
    amount_sats = int(content['amount']) / 1000
    payment_received = {'payment_hash':content['payment_hash'], 'amount': amount_sats, 'username':username, 'timestamp':time.time()}
    set_obj_redis(content['payment_hash'], payment_received)
    hset_redis('notifications', content['payment_hash'], amount_sats )
    print(f"payment: {payment_received}")
    return payment_received



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





