import time
import random

from api.my_client import HuobiClient
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name, \
    minimum_trading_amount, main_trading_token
from huobi_api_master.get_trading_volume_for_period import get_trading_volume_for_specific_account
from huobi_api_master.get_USDT_balance import get_USDT_balance_for_specific_account
from huobi_api_master.market_buy_market_sell import market_buy, market_sell


def main():
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            print('row: ', row, ' ads acc: ', profile_data['ads_acc_num'], ' STARTED')

            client = HuobiClient(api_key=profile_data['access_key'], api_secret=profile_data['secret_key'],
                                 proxy=profile_data['proxy'])

            starting_trading_volume = get_trading_volume_for_specific_account(client=client, row=row)
            have_to_trade_minimum = minimum_trading_amount - starting_trading_volume

            if have_to_trade_minimum < 0:
                print('Traded enough!')
                continue

            print('Start trading volume: ', starting_trading_volume, 'Have to trade: ', have_to_trade_minimum, end='')

            current_usdt_balance = get_USDT_balance_for_specific_account(client=client, row=row)
            maximum_per_one_trade = round(float(current_usdt_balance * 0.9), 2)
            trading_cycles = have_to_trade_minimum / (maximum_per_one_trade * 2)

            for i in range(1, trading_cycles + 1):
                market_buy(client=client, min_amount=maximum_per_one_trade, token=main_trading_token)
                time.sleep(random.randint(1, 2))
                market_sell(client=client, token=main_trading_token)
                time.sleep(random.randint(2, 3))

            print('   SUCCESS!!!')

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    main()
