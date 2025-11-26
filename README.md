# Binance Futures Trading Bot (CLI-Based)
This project is a command-line trading bot for **Binance USDT-M Futures Testnet**, built as part of a Python Developer assignment.  
It supports multiple order types including Market, Limit, Stop-Limit, OCO, TWAP, and Grid Trading.
## Features
### **1. Core (Mandatory)**
- Market Orders  
- Limit Orders  
- Input validation  
- Structured logging to `bot.log`  
### **2. Advanced (Bonus)**
- Stop-Limit Orders  
- OCO (One-Cancels-the-Other: TP + SL)  
- TWAP (Time-Weighted Average Price execution)  
- Grid Trading Strategy (simple implementation)  
## Project Structure
shipra-binance-bot/
|
|- src/
| |- utils.py
| |- market_orders.py
| |- limit_orders.py
| |- advanced/
| |- oco.py
| |- stop_limit.py
| |- twap.py
| |- grid.py
|
|- bot.log
|- report.pdf
|- README.md
|- Instructions_Python_Developer.pdf
