from datetime import datetime

from api.my_client import HuobiClient
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name
from working_data import trading_per_start, trading_tokens, minimum_trading_amount
from general_functions.colors import color


def get_trading_volume_for_all_accounts():
    search_markets = tuple([token + 'usdt' for token in trading_tokens])
    trading_period_start = datetime(trading_per_start['year'], trading_per_start['month'], trading_per_start['day'])

    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            client = HuobiClient(api_key=profile_data['access_key'], api_secret=profile_data['secret_key'],
                                 proxy=profile_data['proxy'])
            account_trading_volume = client.get_traded_amount_in_usdt_for_the_period(
                start_time=trading_period_start, markets=search_markets)
            print(profile_data['ads_acc_num'], ':', round(account_trading_volume, 2))
            if account_trading_volume < minimum_trading_amount:
                print(color['red'] + 'CHECK ACCOUNT:', profile_data['ads_acc_num'], color['reset'])

        except Exception as err:
            print('Row', row, 'error :::', err)


def get_trading_volume_for_specific_account(client, row):
    search_markets = tuple([token + 'usdt' for token in trading_tokens])
    trading_period_start = datetime(trading_per_start['year'], trading_per_start['month'], trading_per_start['day'])

    try:
        account_trading_volume = client.get_traded_amount_in_usdt_for_the_period(
            start_time=trading_period_start, markets=search_markets)
        return round(account_trading_volume, 2)

    except Exception as err:
        print('Row', row, 'error :::', err)


if __name__ == "__main__":
    get_trading_volume_for_all_accounts()
