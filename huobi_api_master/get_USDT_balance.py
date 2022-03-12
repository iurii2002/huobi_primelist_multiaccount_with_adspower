from api.my_client import HuobiClient
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name


def get_USDT_balance_for_all_accounts():
    total_usdt_balance = 0
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            client = HuobiClient(api_key=profile_data['access_key'], api_secret=profile_data['secret_key'],
                                 proxy=profile_data['proxy'])

            token_balance = round(float(client.get_account_balance_by_token('USDT')), 2)
            print(profile_data['ads_acc_num'], ' USDT amount: ', token_balance)
            total_usdt_balance += int(token_balance)

        except Exception as err:
            print('Row', row, 'error :::', err)

    print('TOTAL USDT Balance: ', total_usdt_balance)


def get_USDT_balance_for_specific_account(client, row):
    try:
        token_balance = round(float(client.get_account_balance_by_token('USDT')), 2)
        return token_balance

    except Exception as err:
        print('Row', row, 'error :::', err)


if __name__ == "__main__":
    get_USDT_balance_for_all_accounts()
