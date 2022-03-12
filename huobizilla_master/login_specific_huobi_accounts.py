from clients.huobizilla import HuobiZilla
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from general_functions.get_iterable_list import get_iterable


def login_specific(accounts_number_rows):
    for row in get_iterable(accounts_number_rows):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue

            client = HuobiZilla(mail=profile_data['mail'], huobi_pass=profile_data['huobi_pass'],
                                ads_acc_num=profile_data['ads_acc_num'], ads_acc_id=profile_data['ads_acc_id'],
                                tot_secret=profile_data['tot'])

            client.login()

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    accounts_number = [240]    # account number is the number of row in the file
    login_specific(accounts_number)
