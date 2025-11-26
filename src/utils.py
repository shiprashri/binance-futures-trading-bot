import os
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.log")

def setup_logger():
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RotatingFileHandler(LOG_FILE, maxBytes=2*1024*1024, backupCount=1)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger()
 
def validate_symbol(symbol):
    if not isinstance(symbol, str) or len(symbol) < 4:
        raise ValueError("Invalid symbol format.")
    return symbol.upper()

def validate_side(side):
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be BUY or SELL.")
    return side

def validate_quantity(qty):
    try:
        q = float(qty)
        if q <= 0:
            raise ValueError()
        return q
    except:
        raise ValueError("Quantity must be a positive number.")

def validate_price(price):
    try:
        p = float(price)
        if p <= 0:
            raise ValueError()
        return p
    except:
        raise ValueError("Price must be a positive number.")
def get_client():
    """
    Returns a Binance Futures client connected to TESTNET.
    """
    try:
        from binance.client import Client
    except:
        logger.error("python-binance not installed. Install using: pip install python-binance")
        return None

    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_SECRET_KEY")

    if not api_key or not api_secret:
        logger.error("API keys not set in environment variables.")
        return None

    client = Client(api_key, api_secret, testnet=True)

    # OVERRIDE ALL FUTURES ENDPOINTS TO TESTNET
    client.FUTURES_URL = "https://testnet.binancefuture.com"
    client.futures_api_url = "https://testnet.binancefuture.com/fapi"
    client.FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"

    return client

