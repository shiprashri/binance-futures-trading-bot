import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from utils import (
    validate_symbol,
    validate_quantity,
    validate_price,
    get_client,
    logger
)
def place_stop_limit(symbol, quantity, stop_price, limit_price):
    client = get_client()

    if client is None:
        print("Binance client not available. Install python-binance and set API keys.")
        return

    logger.info(f"Placing STOP-LIMIT order: {symbol} qty={quantity} stop={stop_price} limit={limit_price}")

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side="SELL",            
            type="STOP",
            stopPrice=str(stop_price),
            price=str(limit_price),
            quantity=quantity,
            timeInForce="GTC"
        )

        logger.info(f"Stop-Limit Order Response: {response}")
        print("Stop-Limit Order placed:", response)

    except Exception as e:
        logger.exception("Error placing stop-limit order")
        print("Error:", e)
def main():
    parser = argparse.ArgumentParser(description="Place a STOP-LIMIT order")
    parser.add_argument("symbol")
    parser.add_argument("quantity")
    parser.add_argument("stop_price")
    parser.add_argument("limit_price")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        quantity = validate_quantity(args.quantity)
        stop_price = validate_price(args.stop_price)
        limit_price = validate_price(args.limit_price)

        place_stop_limit(symbol, quantity, stop_price, limit_price)

    except Exception as e:
        logger.error(f"Validation Error: {e}")
        print("Validation Error:", e)
if __name__ == "__main__":
    main()
