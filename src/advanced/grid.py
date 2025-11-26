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
def generate_grid_levels(lower_price, upper_price, grid_size):
    lower = float(lower_price)
    upper = float(upper_price)
    size = int(grid_size)

    if lower >= upper:
        raise ValueError("Lower price must be less than upper price.")
    if size <= 0:
        raise ValueError("Grid size must be a positive integer.")

    step = (upper - lower) / size
    return [round(lower + i * step, 2) for i in range(size + 1)]
def run_grid(symbol, lower_price, upper_price, grid_size, qty_per_order):
    client = get_client()

    if client is None:
        print("Binance client not available. Install python-binance and set API keys.")
        return

    logger.info(f"Running GRID for {symbol} | Range: {lower_price}-{upper_price} | Grid size={grid_size}")

    try:
        grid_levels = generate_grid_levels(lower_price, upper_price, grid_size)
        logger.info(f"Grid Levels: {grid_levels}")

        print("Generated Grid Levels:")
        for level in grid_levels:
            print(level)
        for i, price in enumerate(grid_levels):
            side = "BUY" if i % 2 == 0 else "SELL"

            try:
                resp = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="LIMIT",
                    price=str(price),
                    quantity=qty_per_order,
                    timeInForce="GTC"
                )
                logger.info(f"Grid Order {side} at {price}: {resp}")
            except Exception as order_error:
                logger.error(f"Grid order failed at {price}: {order_error}")
                # Continue placing other grid orders

    except Exception as e:
        logger.exception("Error running grid strategy")
        print("Error:", e)
def main():
    parser = argparse.ArgumentParser(description="Run a simple Grid Trading Strategy")
    parser.add_argument("symbol")
    parser.add_argument("lower_price")
    parser.add_argument("upper_price")
    parser.add_argument("grid_size")
    parser.add_argument("qty_per_order")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        validate_price(args.lower_price)
        validate_price(args.upper_price)
        validate_quantity(args.qty_per_order)

        run_grid(
            symbol,
            args.lower_price,
            args.upper_price,
            args.grid_size,
            args.qty_per_order
        )

    except Exception as e:
        logger.error(f"Validation Error: {e}")
        print("Validation Error:", e)
if __name__ == "__main__":
    main()
