from clients.huobizilla import HuobiZilla
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from general_functions.get_iterable_list import get_iterable


def login_specific(accounts_number_rows):
    for row in get_iterable(accounts_number_rows):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue

            print(profile_data)

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    # account number is the number of account row in the file
    accounts_number = [1, 2, 3, 4]
    login_specific(accounts_number)
