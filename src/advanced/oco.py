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
def place_oco(symbol, quantity, take_profit_price, stop_loss_price):
    client = get_client()

    if client is None:
        print("Binance client not available. Install python-binance and set API keys.")
        return

    logger.info(f"Placing OCO-like orders: {symbol} qty={quantity} TP={take_profit_price} SL={stop_loss_price}")

    try:
        tp_order = client.futures_create_order(
            symbol=symbol,
            side="SELL",
            type="TAKE_PROFIT_MARKET",
            stopPrice=str(take_profit_price),
            quantity=quantity
        )
        sl_order = client.futures_create_order(
            symbol=symbol,
            side="SELL",
            type="STOP_MARKET",
            stopPrice=str(stop_loss_price),
            quantity=quantity
        )

        logger.info(f"TP Order Response: {tp_order}")
        logger.info(f"SL Order Response: {sl_order}")

        print("OCO-like order placed:")
        print("Take-Profit:", tp_order)
        print("Stop-Loss:", sl_order)

    except Exception as e:
        logger.exception("Error placing OCO-like orders")
        print("Error:", e)
def main():
    parser = argparse.ArgumentParser(description="Place an OCO (Take-Profit + Stop-Loss) order")
    parser.add_argument("symbol")
    parser.add_argument("quantity")
    parser.add_argument("take_profit_price")
    parser.add_argument("stop_loss_price")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        quantity = validate_quantity(args.quantity)
        tp = validate_price(args.take_profit_price)
        sl = validate_price(args.stop_loss_price)

        place_oco(symbol, quantity, tp, sl)

    except Exception as e:
        logger.error(f"Validation Error: {e}")
        print("Validation Error:", e)
if __name__ == "__main__":
    main()
