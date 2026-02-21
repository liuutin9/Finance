from datetime import datetime
from openpyxl import load_workbook
from utils.get_stock_price import get_stock_price_tw, get_stock_price_us, get_exchange_rate_USD
from utils.stock_repo import update_stock_price, get_stocks, get_stock_repo

# update stock repo
stocks = get_stocks()
for stock in stocks['TW']:
    stock_price_info = get_stock_price_tw(stock)
    update_stock_price("TW", stock, stock_price_info['current_price'], stock_price_info['yesterday_price'])
for stock in stocks['US']:
    stock_price_info = get_stock_price_us(stock)
    update_stock_price("US", stock, stock_price_info['current_price'], stock_price_info['yesterday_price'])

update_stock_price("Crypto", "USDT", get_exchange_rate_USD())

# update excel file
wb = load_workbook("帳目表.xlsx")
stock_repo = get_stock_repo()
for stock in stocks['TW']:
    wb[stock]["C3"].value = stock_repo['TW'][stock]['CurrentPrice']
for stock in stocks['US']:
    wb[stock]["H3"].value = stock_repo['US'][stock]['CurrentPrice']
        
wb["投資"]["G2"].value = get_exchange_rate_USD()
    
wb.save("帳目表.xlsx")
wb.close()

with open("stock_repo_log.txt", mode="w", encoding="utf-8") as log:
    now = datetime.now().replace(microsecond=0)
    print(now, file=log)
    print(now)
    print("Stock Repo Update Success!")