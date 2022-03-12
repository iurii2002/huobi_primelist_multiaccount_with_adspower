from clients.huobizilla import HuobiZilla
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from general_functions.get_iterable_list import get_iterable


def login_specific(accounts_number_rows, new_pass):
    for row in get_iterable(accounts_number_rows):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue

            client = HuobiZilla(mail=profile_data['mail'], huobi_pass=profile_data['huobi_pass'],
                                ads_acc_num=profile_data['ads_acc_num'], ads_acc_id=profile_data['ads_acc_id'],
                                tot_secret=profile_data['tot'])

            client.change_huobi_pass(new_pass)

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    # account number is the number of account row in the file
    accounts_number = [1, 2, 3, 4]
    new_pass = 'askdhbkasdha'
    login_specific(accounts_number, new_pass)
