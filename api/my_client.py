import math
import time
import base64
import hashlib
import hmac
import json


from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from requests import Request, Session, Response
from urllib import parse
from urllib.parse import urlencode
from api.builder import UrlParamsBuilder

TWO_DAYS_IN_MILLISECONDS = 172800000


class HuobiClient:
    _ENDPOINT = 'https://api.huobi.pro'

    def __init__(self, api_key=None, api_secret=None, proxy=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._proxy = proxy

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self._request('GET', path=path, headers=headers, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        headers = ({'Content-Type': 'application/json'})
        return self._request('POST', path=path, headers=headers, params=params)

    def _request(self, method: str, path: str, headers: dict, params=None) -> Any:
        request = Request(method, self._ENDPOINT + path, headers=headers)
        self._sign_request(request, params)
        if request.method == 'POST':
            request.data = json.dumps(params)
        response = self._session.send(request.prepare(), proxies=self._proxy)
        return self._process_response(response)

    def _sign_request(self, request: Request, params: Any = None) -> None:
        if self._api_key is None or self._api_secret is None or self._api_key == "" or self._api_secret == "":
            raise EOFError("API key and secret key are required")
        timestamp = str(datetime.utcnow().isoformat())[0:19]

        builder = UrlParamsBuilder()

        if params and len(params):
            if request.method == 'GET':
                for key, value in params.items():
                    builder.put_url(key, value)
            elif request.method == 'POST':
                for key, value in params.items():
                    builder.put_post(key, value)

        builder.put_url("AccessKeyId", self._api_key)
        builder.put_url("SignatureMethod", "HmacSHA256")
        builder.put_url("SignatureVersion", "2")
        builder.put_url("Timestamp", timestamp)

        base_uri = 'api.huobi.pro'
        path = str(request.url.split(base_uri)[1])

        keys = sorted(builder.param_map.keys())
        qs0 = '&'.join(['%s=%s' % (key, parse.quote(builder.param_map[key], safe='')) for key in keys])

        payload0 = request.method + '\n' + base_uri + '\n' + path + '\n' + qs0
        dig = hmac.new(self._api_secret.encode(), payload0.encode(), hashlib.sha256).digest()
        s = urlencode({'Signature': base64.b64encode(dig).decode()})

        request.url += builder.build_url()
        request.url += "&"
        request.url += s

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
            if 'status' in data and data['status'] == 'error':
                raise ValueError(data['err-msg'])
        except ValueError:
            response.raise_for_status()
            raise
        else:
            return data['data']

    def get_account_data(self) -> List[dict]:
        return self._get('/v1/account/accounts')

    def get_spot_account_id(self) -> str:
        all_accs = self.get_account_data()
        for acc in all_accs:
            if acc['type'] == 'spot':
                return acc['id']

    def get_trading_symbols(self):
        return self._get('/v1/common/symbols')

    def get_account_balance(self):
        accounts = self.get_account_data()
        full_balance = []
        for account_item in accounts:
            if account_item['type'] != 'spot':
                continue
            account_id = account_item['id']
            full_balance = self._get(f'/v1/account/accounts/{account_id}/balance')
        return full_balance

    def get_account_balance_by_token(self, token):
        accounts = self.get_account_data()
        full_balance = []
        for account_item in accounts:
            if account_item['type'] != 'spot':
                continue
            account_id = account_item['id']
            full_balance = self._get(f'/v1/account/accounts/{account_id}/balance')

        token_balance = 0

        for balance in full_balance['list']:
            if balance['currency'] == token.lower():
                token_balance += float(balance['balance'])

        return token_balance

    async def async_get_account_balance_by_token(self, token):
        accounts = self.get_account_data()
        full_balance = []
        for account_item in accounts:
            if account_item['type'] == 'point':
                continue
            account_id = account_item['id']
            full_balance = self._get(f'/v1/account/accounts/{account_id}/balance')

        token_balance = 0

        for balance in full_balance['list']:
            if balance['currency'] == token.lower():
                token_balance += float(balance['balance'])

        return token_balance

    def create_order(self, symbol: 'str', account_id: 'str', order_type: 'OrderType', amount: 'float',
                     source: 'str'='spot-api', price: 'float'=None,  client_order_id=None, stop_price=None, operator=None) -> int:

        """
        Make an order in huobi.

        :param symbol: The symbol, like "btcusdt". (mandatory)
        :param account_id: Account id. (mandatory)
        :param order_type: The order type. (mandatory)
        :param source: The order source. (mandatory)
                for spot, it's "api", see OrderSource.API
                for margin, it's "margin-api", see OrderSource.MARGIN_API
                for super margin, it's "super-margin-api", see OrderSource.SUPER_MARGIN_API
        :param amount: The amount to buy (quote currency) or to sell (base currency). (mandatory)
        :param price: The limit price of limit order, only needed for limit order. (mandatory for buy-limit, sell-limit, buy-limit-maker and sell-limit-maker)
        :param client_order_id: unique Id which is user defined and must be unique in recent 24 hours
        :param stop_price: Price for auto sell to get the max benefit
        :param operator: the condition for stop_price, value can be "gte" or "lte",  gte – greater than and equal (>=), lte – less than and equal (<=)
        :return: The order id.
        """

        body = {"symbol": symbol, "account-id": account_id, "type": order_type, "amount": amount}
        return self._post('/v1/order/orders/place', body)

    def place_new_spot_market_order(self, amount: 'float', symbol: 'str', side: 'str'):
        account_id = self.get_spot_account_id()
        type = f'{side}-market'
        return self.create_order(symbol=symbol, account_id=account_id, order_type=type, amount=amount)

    def place_new_spot_limit_order(self):
        pass

    def get_account_history(self, currency=None, start_time=None, end_time=None):
        account_id = self.get_spot_account_id()
        body = {"account-id": account_id, "currency": currency, "start-time": start_time, "end-time": end_time}
        return self._get('/v1/account/history', body)

    def get_full_orders_history(self, currency, start_time=None, end_time=None):
        """
        Get an order history on huobi.

        :param currency: The symbol, like "btcusdt". (Required)
        :param start_time: UTC time in millisecond. Default value - 48 hours ago. (optional)
        :param end_time: UTC time in millisecond. Default value - current time. (optional)
        """

        states = 'filled'  # we can also add 'partial-canceled' state if we have such type of orders
        body = {"symbol": currency, "start-time": start_time, "end-time": end_time, 'states': states}

        return self._get('/v1/order/orders', body)

    def get_traded_amount_in_usdt_for_the_period(self, markets=tuple(['btcusdt']), start_time=None, end_time=None):
        total_trading_amount = 0

        start_time, end_time = \
            self.convert_datetime_to_milliseconds(start_time), self.convert_datetime_to_milliseconds(end_time)
        current_time = self.current_milli_time()
        if not end_time or end_time > current_time:
            end_time = current_time

        searching_period = end_time - start_time

        requests_needed = math.ceil(searching_period / TWO_DAYS_IN_MILLISECONDS)
        for market in markets:
            total_trading_amount += \
                self.get_traded_amount_in_usdt_for_the_period_of_specific_market(requests_needed, market, start_time, end_time)
        return total_trading_amount

    async def async_get_traded_amount_in_usdt_for_the_period(self, markets=tuple(['btcusdt']), start_time=None, end_time=None):
        total_trading_amount = 0

        start_time, end_time = \
            self.convert_datetime_to_milliseconds(start_time), self.convert_datetime_to_milliseconds(end_time)
        current_time = self.current_milli_time()
        if not end_time or end_time > current_time:
            end_time = current_time

        searching_period = end_time - start_time

        requests_needed = math.ceil(searching_period / TWO_DAYS_IN_MILLISECONDS)
        for market in markets:
            total_trading_amount += \
                self.get_traded_amount_in_usdt_for_the_period_of_specific_market(requests_needed, market, start_time, end_time)
        return total_trading_amount

    def get_traded_amount_in_usdt_for_the_period_of_specific_market(self, requests_needed, market, start_time, end_time):
        this_market_trading_amount = 0
        for _ in range(0, requests_needed):
            this_market_trading_amount += self._process_trading_amounts_data(
                self.get_full_orders_history(currency=market, start_time=start_time,
                                             end_time=min(start_time+TWO_DAYS_IN_MILLISECONDS, end_time)))
            start_time += TWO_DAYS_IN_MILLISECONDS
        return this_market_trading_amount

    def _get_market_data(self):
        return self._get('/v1/common/symbols')

    def get_market_precision(self, market):
        all_markets = self._get_market_data()
        for m in all_markets:
            if m['symbol'] == market:
                return m['amount-precision']

    def _get_user_UID(self):
        return self._get('/v2/user/uid')

    def get_deposit_address(self, currency):
        body = {"currency": currency}
        wallets = self._get('/v2/account/deposit/address', body)
        for wallet in wallets:
            if wallet['chain'] == 'trc20usdt':
                return wallet['address']

    @staticmethod
    def _process_trading_amounts_data(trades):
        if not trades or len(trades) < 1:
            return 0
        return sum([float(trade['field-cash-amount']) for trade in trades])

    @staticmethod
    def current_milli_time():
        return int(round(time.time() * 1000))

    @staticmethod
    def convert_datetime_to_milliseconds(dt):
        if isinstance(dt, datetime):
            return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)
        elif isinstance(dt, float):
            return int(dt)
        else:
            return None
