import keyring

from function import check_kraken_status, create_market_order
from constant import dca_strategy, _keyring_service_name, _api_key_username, _api_secret_username


# Check if Kraken is online before sending orders
check_kraken_status()

# Get the API key and secret from the keyring library
api_key = keyring.get_password(_keyring_service_name, _api_key_username)
api_sec = keyring.get_password(_keyring_service_name, _api_secret_username)

for asset in dca_strategy:
    order = create_market_order(asset['pair'], asset['amount'], api_key, api_sec)
    print(order['result']['descr']['order'])

# Add something to keep log of each order
