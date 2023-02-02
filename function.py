import sys
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
import smtplib

from constant import api_url


def check_kraken_status():
    resp = requests.get('https://api.kraken.com/0/public/SystemStatus')
    kraken_status = resp.json()['result']['status']
    if kraken_status != 'online':
        sys.exit(0)


# return the API-Sign header as defined in the 'Authentication' section (see Kraken doc)
def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, key, secret):
    headers = {
        'API-Key': key,
        'API-Sign': get_kraken_signature(uri_path, data, secret)
    }
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req


def get_balance(key, secret):
    data = {'nonce': str(int(1000*time.time()))}
    resp = kraken_request('/0/private/Balance', data, key, secret)
    return {key: float(value) for key, value in resp.json()['result'].items() if float(value) > 0.001}


def get_ask_price(pair):
    resp = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair}').json()
    ask_price = resp['result'][pair]['a'][0]
    return float(ask_price)


def create_market_order(pair, to_invest, api_key, api_sec):
    ask_price = get_ask_price(pair)
    qty = to_invest/ask_price
    data = {
        'nonce': str(int(1000 * time.time())),
        'userref': 1,
        'ordertype': 'market',
        'type': 'buy',
        'volume': qty,
        'pair': pair,
    }
    resp = kraken_request('/0/private/AddOrder', data, api_key, api_sec)
    return resp.json(), ask_price


def send_email(receiver, subject, msg, pwd):
    sender = 'lucbesset.95@gmail.com'
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, pwd)
        msg = f"Subject: {subject}\n\n{msg}"
        server.sendmail(sender, receiver, msg.encode('utf-8'))
        server.quit()
    except Exception as e:
        print(f"Error: Unable to send email to {receiver}. {e}")
