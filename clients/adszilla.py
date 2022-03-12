import time

import requests
from selenium import webdriver


def check_if_open(ads_acc_id: str) -> bool:
    time.sleep(1)
    check_url = "http://local.adspower.net:50325/api/v1/browser/active?user_id=" + ads_acc_id
    resp = requests.get(check_url).json()
    if resp["data"]["status"] == 'Active':
        return True
    else:
        return False


def get_proxy(group_id=None, ads_acc_id=None, serial_number=None, page=None, page_size=None):
    url = 'http://localhost:50325/api/v1/user/list'
    options = {
            'group_id': group_id,
            'user_id': ads_acc_id,
            'serial_number': serial_number,
            'page': page,
            'page_size': page_size
        }
    response = requests.get(url, params=options).json()
    return response


class AdsZilla:
    def __init__(self, ads_acc_num: int, ads_acc_id: str, proxy_ip: str = None, proxy_port: int = None,
                 proxy_login: str = None, proxy_psw: str = None):

        self.acc_num = ads_acc_num
        self.acc_id = ads_acc_id
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.proxy_login = proxy_login
        self.proxy_psw = proxy_psw
        self.driver = self._start_driver()

    def _start_driver(self):
        open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + self.acc_id
        resp = requests.get(open_url).json()
        chrome_driver = resp["data"]["webdriver"]
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        return driver

    def close_all_pages_except_main(self):
        original_handle = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if handle != original_handle:
                self.driver.switch_to.window(handle)
                self.driver.close()

        self.driver.switch_to.window(original_handle)

    def close_browser(self):
        close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + self.acc_id
        self.driver.quit()
        requests.get(close_url)

    def redirect_to_page(self, site_url):
        self.driver.get(site_url)
