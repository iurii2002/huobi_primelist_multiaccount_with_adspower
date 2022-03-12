# HUOBI DATA CONFIG
working_file = r''  # link to working file
data_columns = {
        'mail': 2,
        'mail_pass': 3,
        'huobi_pass': 4,
        'ads_acc_num': 5,
        'ads_acc_id': 6,
        'tot': 7,
        'ads_group': 8,
        'trc': 9,
        'access_key': 10,
        'secret_key': 11,
        'proxy_ip': 12,
        'proxy_user': 13,
}

# ADS CONFIG
starting_account = 1  # starting row from the working file above
number_of_accounts = 600  # total number of account to process
acc_group_name = ['']  # group name to open on this server instance, placed in the ads_group column in working file

# SALE CONFIG
sale_link = ''  # for example https://www.huobi.com/en-us/topic/primelist/?code=STORE
minimum_USDT_holding = 50
sale_token = ''  #  primelist token ticker, e.g. STORE
main_trading_token = ''  # token that you will trade to get trading volume, e.g. btc or eth
minimum_trading_amount = 1200  # trading amount needed to participate in primelist
trading_per_start = {'year': 2022, 'month': 1, 'day': 22}  # huobi trading period start to calculate trade amounts
trading_tokens = ['btc']  # huobi tokens to calculate trading amount
spin_link = ''  # link to huobi spin page, like https://www.huobi.com/en-us/topic/trading-activity-tmpl/?code=Lottery220112154956
miner_link = ''  # link to huobi miner page, like https://www.huobi.com/en-us/topic/mining/

# ANTI-CAPTCHA CONFIG
anti_captcha_key = ''  # https://anti-captcha.com/ key to solve log-in captcha
