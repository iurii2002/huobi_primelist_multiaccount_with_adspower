import math
import random
import asyncio
import time

from api.my_client import HuobiClient
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name, \
    minimum_trading_amount, main_trading_token
from huobi_api_master.get_trading_volume_for_period import get_trading_volume_for_specific_account
from huobi_api_master.get_USDT_balance import get_USDT_balance_for_specific_account
from huobi_api_master.market_buy_market_sell import market_buy, market_sell
from general_functions.colors import color


async def trade_necessary_amount(client, row, ads_acc_num, have_to_trade_minimum, starting_trading_volume):
    try:
        if have_to_trade_minimum <= 0:
            print(color['green'] + 'Row: ', row, ' ads acc: ', ads_acc_num,
                  f'Traded enough - {starting_trading_volume}' + color['reset'])
            return

        print('Row: ', row, ' ads acc: ', ads_acc_num, ' start trading volume: ', starting_trading_volume,
              ' have to trade: ', have_to_trade_minimum)

        current_usdt_balance = get_USDT_balance_for_specific_account(client=client, row=row)
        maximum_per_one_trade = math.floor(float(current_usdt_balance * 0.9))
        trading_cycles = math.ceil((have_to_trade_minimum / maximum_per_one_trade) / 2)
        amount_per_trade = round((have_to_trade_minimum / trading_cycles) / 2, 2)

        for i in range(1, trading_cycles + 1):
            market_buy(client=client, min_amount=amount_per_trade, token=main_trading_token)
            print('Row: ', row, ' ads acc: ', ads_acc_num, ' market buy ', amount_per_trade, 'USDT for', main_trading_token)
            time.sleep(1)
            market_sell(client=client, token=main_trading_token)
            print('Row: ', row, ' ads acc: ', ads_acc_num, ' market sell ', main_trading_token)
            await asyncio.sleep(random.randint(1, 20))

        print(color['green'] + 'Row: ', row, ' ads acc: ', ads_acc_num, '   SUCCESS!!!' + color['reset'])
    except Exception as err:
        print(color['red'] + 'Row: ', row, ' ads acc: ', ads_acc_num, err, color['reset'])
        return


async def main():
    list_of_coroutines = []
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            client = HuobiClient(api_key=profile_data['access_key'], api_secret=profile_data['secret_key'],
                                 proxy=profile_data['proxy'])

            print('Row: ', row, ' ads acc: ', profile_data['ads_acc_num'], ' STARTED')

            starting_trading_volume = get_trading_volume_for_specific_account(client=client, row=row)

            if starting_trading_volume is None:  # in this something wrong with api client
                return

            have_to_trade = minimum_trading_amount - starting_trading_volume

            list_of_coroutines.append(trade_necessary_amount(client=client, row=row,
                                                             ads_acc_num=profile_data['ads_acc_num'],
                                                             have_to_trade_minimum=have_to_trade,
                                                             starting_trading_volume=starting_trading_volume))

            if len(list_of_coroutines) == 10:
                await asyncio.gather(*list_of_coroutines)
                list_of_coroutines = []

        except Exception as err:
            print('Row', row, 'error :::', err)

    await asyncio.gather(*list_of_coroutines)


if __name__ == "__main__":
    asyncio.run(main())
