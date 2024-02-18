import requests
from bs4 import BeautifulSoup
import json
from openpyxl import Workbook, load_workbook
import schedule
import time

def get_stock_price(symbol):
    url = f"https://tw.finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("div", {"class": "D(f) Ai(fe) Mb(4px)"}).find("span")
        if price_element:
            return price_element.text
        else:
            return "Price not found"
    else:
        return "Failed to fetch data"
    
def get_exchange_rate_USD():
    url = 'https://mma.sinopac.com/ws/share/rate/ws_exchange.ashx'

    headers = {
        'Authorization': 'Bearer your_api_key',
    }

    params = {
        'Lang': 'zh-TW',
        'Currency': 'USD',
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.content)
    
    return float(data[0]['SubInfo'][0]['DataValue2'])



wb = load_workbook("帳目表.xlsx")

# 股票代碼
stock_symbols = ["006208.TW", "00692.TW", "00878.TW", "2890.TW", "BND", "VEA", "VT", "VTI"]

# 獲取股價
stock_prices = {}

# modify excel file
for symbol in stock_symbols:
    if (symbol[len(symbol)-3] == '.'):
        wb[symbol]["C3"].value = get_stock_price(symbol)
    else:
        wb[symbol]["H3"].value = get_stock_price(symbol)
        
wb["投資"]["G2"].value = get_exchange_rate_USD()
    
wb.save("帳目表.xlsx")
    
# 寫入 txt 檔
# out = open("stock_prices.txt", mode = "w")
# for i in range(len(stock_symbols)):
#     out.write(f"{stock_symbols[i]},{stock_prices[i]}\n")
# out.write(f"USD,{exchange_rate_USD}\n")
# out.close()

# print("股價已成功寫入 stock_prices.txt 檔案中.")

print("Success!")