from api.my_client import HuobiClient
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name


def get_all_token_balance_for_all_accounts():
    total_balances = {}
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            client = HuobiClient(api_key=profile_data['access_key'], api_secret=profile_data['secret_key'],
                                 proxy=profile_data['proxy'])

            account_balances = client.get_account_balance()['list']
            for balance in account_balances:
                if float(balance['balance']) == 0.0:
                    continue
                if balance['currency'] in total_balances:
                    total_balances[balance['currency']] += float(balance['balance'])
                else:
                    total_balances[balance['currency']] = float(balance['balance'])

            print('Ads accpunt:', profile_data['ads_acc_num'], ' balances: ', total_balances)

        except Exception as err:
            print('Row', row, 'error :::', err)


def get_all_token_balance_for_specific_account(client, row):
    try:
        profile_data = get_account_data_from_file(row)
        if not profile_data:
            return
        if profile_data['ads_group'] not in acc_group_name:
            return

        token_balances = client.get_account_balance()['list']
        total_balances = {}
        for balance in token_balances:
            if float(balance['balance']) == 0.0:
                continue
            if balance['currency'] in total_balances:
                total_balances[balance['currency']] += float(balance['balance'])
            else:
                total_balances[balance['currency']] = float(balance['balance'])

        return total_balances

    except Exception as err:
        print('Row', row, 'error :::', err)


if __name__ == "__main__":
    get_all_token_balance_for_all_accounts()
