from clients.huobizilla import HuobiZilla
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name


def print_all():
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            print(profile_data)

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    print_all()
