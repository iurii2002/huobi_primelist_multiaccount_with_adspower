import math
import random

from my_client import *


class APIzilla(HuobiClient):

    def __int__(self, ads_num: str, token: str = 'btc', min_trade_amount: float = 33.5):

        super().__init__()
        self.token = token
        self.min_trade_amount = min_trade_amount
        self.ads_num = ads_num

    def buy_token(self) -> None:
        amount = round(random.uniform(self.min_trade_amount, self.min_trade_amount + 2), 2)
        self.place_new_spot_market_order(amount=amount, symbol=self.token+'usdt', side='buy')

    def sell_token(self) -> None:
        amount = math.floor(self.get_account_balance_by_token(self.token) * 1000000) / 1000000
        self.place_new_spot_market_order(amount=amount, symbol=self.token+'usdt', side='sell')

    def print_balances(self) -> None:
        print('USDT balance: ', self.get_account_balance_by_token('UsdT'))
        print(f'{self.token} balance: ', self.get_account_balance_by_token(self.token))

    def check_that_have_50_usdt(self) -> bool:
        usdt_bal = self.get_account_balance_by_token('UsdT')
        if usdt_bal < 50:
            print('Ads acc: ', self.ads_num, ' Not enough balance: ', round(usdt_bal, 2))
            return False
        else:
            print(self.ads_num, ' : ', round(usdt_bal, 2))
            return True

    def trade_minimum(self) -> bool:
        """
        possible markets - 'ethusdt', 'btcusdt'
        buy - to buy left part of the symbol
        sell - to sell left part of the symbol
        """
        for i in range(1, 4):
            self.buy_token()
            time.sleep(random.randint(5, 10))
            self.sell_token()
            time.sleep(random.randint(10, 20))
        time.sleep(random.randint(10, 20))
        return True
