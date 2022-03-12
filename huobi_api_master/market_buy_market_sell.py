import random
import math

from working_data import main_trading_token


def market_buy(client, min_amount: float, token=main_trading_token):
    market = token + 'usdt'
    if min_amount < 5:
        min_amount = 5
    amount = round(random.uniform(min_amount, min_amount*1.005), 2)
    client.place_new_spot_market_order(amount=amount, symbol=market, side='buy')


def market_sell(client, token=main_trading_token, amount=None):
    market = token + 'usdt'
    if not amount:
        amount = math.floor(client.get_account_balance_by_token(token) * 1000000) / 1000000
    client.place_new_spot_market_order(amount=amount, symbol=market, side='sell')
