import keyring
import pandas as pd
import datetime as dt
import os

from function import check_kraken_status, create_market_order, send_email
from constant import dca_strategy, receiver_email, root, _kraken_service_name, _api_key_user, _api_secret_user, \
    _gmail_service_name, _gmail_user


# Check if Kraken is online before sending orders
check_kraken_status()

# Get the API key and secret from the keyring library
api_key = keyring.get_password(_kraken_service_name, _api_key_user)
api_sec = keyring.get_password(_kraken_service_name, _api_secret_user)
pwd = keyring.get_password(_gmail_service_name, _gmail_user)

log = []
for asset in dca_strategy:
    order, price = create_market_order(asset['pair'], asset['amount'], api_key, api_sec)

    tday = dt.datetime.today()
    if not order['error']:
        way, qty, pair, at, order_type = order['result']['descr']['order'].split(' ')
        subject = f"DCA Kraken - {asset['ticker']} {round(price, 0)}"
        msg = order['result']['descr']['order'].replace(asset['pair'], asset['ticker'])
        msg += f" [{round(float(qty) * price, 2)}€]\n{tday.strftime('%b %d, %Y (%H:%M)')}"
        send_email(receiver_email, subject, msg, pwd)

        log.append({
            'Date': tday,
            'way': way,
            'type': order_type,
            'ticker': asset['ticker'],
            'qty': qty,
            'unit_price': price,
            'price': float(qty) * price,
        })
    else:
        subject = f"[FAIL] DCA Kraken - {asset['ticker']} {round(price, 0)}"
        msg = f"{asset['ticker']}: {order['error']}\n{tday.strftime('%b %d, %Y (%H:%M)')}"
        send_email(receiver_email, subject, msg, pwd)

if os.path.exists(root + 'log/logs.pkl'):
    logs = pd.read_pickle(root + 'log/logs.pkl')
    log_df = pd.DataFrame(log)
    logs = pd.concat([logs, log_df], ignore_index=True)
else:
    logs = pd.DataFrame(log)
logs.to_pickle(root + 'log/logs.pkl')
