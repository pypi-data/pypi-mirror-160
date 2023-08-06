import pyotp
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException


def get_totp(secret: str) -> str:
    """
    Fetches the T-OTP from Google Authenticator
    """
    return pyotp.TOTP(secret).now()


def is_logged_in(kite: KiteConnect) -> bool:
    """
    Since, KiteConnect doesn't provide a clean way to check if the access token is valid. We will try to fetch the price
    of an instrument and see if a valid response is return. If we see a status code of 403 , it means that the session
    is expired. Check https://kite.trade/docs/connect/v3/exceptions/#common-http-error-codes to learn about error codes.

    @:return True if the KiteConnect is still valid
    """
    try:
        kite.ltp("NSE:INFY")
    except KiteException as ke:
        if ke.code == 403:
            return False
        raise ke
    return True
