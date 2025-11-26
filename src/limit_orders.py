import argparse
from utils import (
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    get_client,
    logger
)
def place_limit_order(symbol, side, quantity, price):
    client = get_client()

    if client is None:
        print("Binance client not available. Install python-binance and set API keys.")
        return

    logger.info(f"Placing LIMIT order: {symbol} {side} {quantity} @ {price}")

    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price)
        )

        logger.info(f"Order Response: {response}")
        print("Limit Order placed:", response)

    except Exception as e:
        logger.exception("Error placing limit order")
        print("Error:", e)
def main():
    parser = argparse.ArgumentParser(description="Place a Binance Futures LIMIT order")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("quantity")
    parser.add_argument("price")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)

        place_limit_order(symbol, side, quantity, price)

    except Exception as e:
        logger.error(f"Validation Error: {e}")
        print("Validation Error:", e)


if __name__ == "__main__":
    main()
