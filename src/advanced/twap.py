import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
import time
from utils import (
    validate_symbol,
    validate_side,
    validate_quantity,
    get_client,
    logger
)

def twap_execute(symbol, side, total_qty, chunks, interval_seconds):
    """
    Execute a TWAP: split `total_qty` into `chunks` equal pieces,
    place one market order per chunk, sleeping `interval_seconds`
    between chunks.
    """
    client = get_client()
    if client is None:
        print("Binance client not available. Install python-binance and set API keys.")
        return

    try:
        chunks = int(chunks)
        if chunks <= 0:
            raise ValueError("chunks must be a positive integer")
        interval_seconds = float(interval_seconds)
        if interval_seconds < 0:
            raise ValueError("interval_seconds must be >= 0")
    except Exception as e:
        logger.error(f"TWAP argument error: {e}")
        print("TWAP argument error:", e)
        return

    qty_per_chunk = float(total_qty) / chunks
    logger.info(f"Starting TWAP: {symbol} {side} total={total_qty} chunks={chunks} qty/chunk={qty_per_chunk} interval={interval_seconds}s")

    for i in range(chunks):
        logger.info(f"TWAP chunk {i+1}/{chunks}: placing MARKET order qty={qty_per_chunk}")
        try:
            resp = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty_per_chunk
            )
            logger.info(f"TWAP chunk response: {resp}")
            print(f"Chunk {i+1}/{chunks} response:", resp)
        except Exception as e:
            logger.exception("Error executing TWAP chunk")
            print("Error executing chunk:", e)
        if i < chunks - 1:
            time.sleep(interval_seconds)

    logger.info("TWAP completed.")
def main():
    parser = argparse.ArgumentParser(description="TWAP execution: split order into chunks over time")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("total_qty")
    parser.add_argument("chunks", help="Number of chunks to split into (integer)")
    parser.add_argument("interval_seconds", help="Seconds to wait between chunks (float)")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        total_qty = validate_quantity(args.total_qty)
        twap_execute(symbol, side, total_qty, args.chunks, args.interval_seconds)
    except Exception as e:
        logger.error(f"Validation Error: {e}")
        print("Validation Error:", e)


if __name__ == "__main__":
    main()
