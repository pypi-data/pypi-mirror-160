from selenium.common.exceptions import *
from urllib.error import URLError

# --- Exceptions Selenium Base ---- #
class TimeoutException(TimeoutException):
    pass


class WebDriverException(WebDriverException):
    pass


class ElementClickInterceptedException(ElementClickInterceptedException):
    pass
# --- Exceptions Selenium Base ---- #


# --- Exceptions Python Base ---- #
class EmailOuLoginIncorretoElawException(Exception):
    pass

class EmailOuLoginIncorretoGmailException(Exception):
    pass
# --- Exceptions Python Base ---- #


# --- Exceptions urllib Base ---- #
class ErroNaURLUrllib(URLError):
    pass


