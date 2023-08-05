"""Constants used across the project."""

try:
    from importlib_metadata import version
except ImportError:
    # >= py 3.8
    from importlib.metadata import version

CAIRO_LANG_VERSION = version("cairo-lang")
FAILURE_REASON_KEY = "transaction_failure_reason"
TIMEOUT_FOR_WEB3_REQUESTS = 120 #seconds
L1_MESSAGE_CANCELLATION_DELAY = 0 # Min amount of time in seconds for a message to be able to be cancelled

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5050

DEFAULT_ACCOUNTS = 10
DEFAULT_INITIAL_BALANCE = 10 ** 21
DEFAULT_GAS_PRICE = 10 ** 11
