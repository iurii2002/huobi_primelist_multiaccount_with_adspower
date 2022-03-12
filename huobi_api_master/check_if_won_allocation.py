from api.my_client import HuobiClient
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name, sale_token


def main():
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            client = HuobiClient(api_key=profile_data['access_key'], api_secret=profile_data['secret_key'],
                                 proxy=profile_data['proxy'])

            token_balance = client.get_account_balance_by_token(sale_token)

            if token_balance > 1:
                print('Ads acc: ', profile_data['ads_acc_num'], ' WON')
            else:
                pass

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    main()
