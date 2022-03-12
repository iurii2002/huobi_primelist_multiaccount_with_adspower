import pyotp


def get_totp(secret):
    totp = pyotp.TOTP(secret).now()
    return totp


if __name__ == "__main__":
    secret = 'PBUMZ43VZ7J6VU2T'
    print(get_totp(secret))
