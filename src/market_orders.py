import argparse
from utils import (
    validate_symbol,
    validate_side,
    validate_quantity,
    get_client,
    logger
)
def place_market_order(symbol, side, quantity):
    client = get_client()

    if client is None:
        print("Binance client not available. Install python-binance and set API keys.")
        return

    logger.info(f"Placing MARKET order: {symbol} {side} {quantity}")

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        logger.info(f"Order Response: {response}")
        print("Order placed:", response)

    except Exception as e:
        logger.exception("Error placing market order")
        print("Error:", e)
def main():
    parser = argparse.ArgumentParser(description="Place a Binance Futures MARKET order")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("quantity")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)

        place_market_order(symbol, side, quantity)

    except Exception as e:
        logger.error(f"Validation Error: {e}")
        print("Validation Error:", e)
if __name__ == "__main__":
    main()
