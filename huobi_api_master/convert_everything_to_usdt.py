import math

from api.my_client import HuobiClient
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name
from huobi_api_master.get_all_tokens_balance import get_all_token_balance_for_specific_account
from huobi_api_master.market_buy_market_sell import market_sell


def main():
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            print('row: ', row, ' ads acc: ', profile_data['ads_acc_num'], ' STARTED', end='')

            client = HuobiClient(api_key=profile_data['access_key'], api_secret=profile_data['secret_key'],
                                 proxy=profile_data['proxy'])

            current_total_balance = get_all_token_balance_for_specific_account(client=client, row=row)

            for token, amount in current_total_balance.items():
                if token == 'usdt':
                    continue
                try:
                    precision = client.get_market_precision(token+'usdt')
                    multiplier = int('1' + '0' * precision)
                    amount = math.floor(amount * multiplier) / multiplier
                    market_sell(client=client, token=token, amount=amount)
                except ValueError:
                    pass

            print('   SUCCESS!!!')

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    main()
