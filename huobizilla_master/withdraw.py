import time

from clients.huobizilla import HuobiZilla
from general_functions.get_account_data_from_excel_file import get_account_data_from_file
from working_data import starting_account, number_of_accounts, acc_group_name


def withdraw_all():
    network = 'sol'
    withdr_adr = '6RNCi1m7wJJMpknDSoxgMz3Li3LoVMcsPSfrYtdpK78C'
    for row in range(starting_account, starting_account + number_of_accounts):
        try:
            profile_data = get_account_data_from_file(row)
            if not profile_data:
                continue
            if profile_data['ads_group'] not in acc_group_name:
                continue

            client = HuobiZilla(mail=profile_data['mail'], huobi_pass=profile_data['huobi_pass'],
                                ads_acc_num=profile_data['ads_acc_num'], ads_acc_id=profile_data['ads_acc_id'],
                                tot_secret=profile_data['tot'])

            client.login()
            time.sleep(2)
            client.withdraw_USDT(withdr_adr, network)
            client.close_browser()

        except Exception as err:
            print('Row', row, 'error :::', err)


if __name__ == "__main__":
    withdraw_all()
