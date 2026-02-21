import requests
import urllib3
import yfinance as yf
from datetime import datetime

# Close SSL verification warnings to keep the terminal output clean
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_exchange_rate_USD() -> float:
    url = "https://rate.bot.com.tw/xrt/flcsv/0/day"
    response = requests.get(url)
    response.encoding = 'utf-8'
    rows = response.text.split('\n')
    rate = rows[1].split(',')[13]  # Assuming the rate is in the 13th column
    return float(rate)

def get_stock_price_tw(symbol:str) -> dict:
    api = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{symbol}.tw&json=1&delay=0'
    response = requests.get(api, verify=False)
    if response.status_code == 200:
        data = response.json()['msgArray'][0]
        rt = {}
        rt['code'] = data['c']
        rt['name'] = data['n']
        rt['time'] = data['t']
        rt['current_price'] = float(data['z'])
        rt['open_price'] = float(data['o'])
        rt['highest_price'] = float(data['h'])
        rt['lowest_price'] = float(data['l'])
        rt['yesterday_price'] = float(data['y'])
        rt['price_change'] = float(rt['current_price']) - float(rt['yesterday_price'])
        rt['price_change_rate'] = (rt['price_change'] / float(rt['yesterday_price'])) * 100 if float(rt['yesterday_price']) != 0 else 0
        return rt
    else:
        return f"Failed to fetch data for {symbol}"
    
def get_stock_price_us(symbol:str) -> dict:
    ticker = yf.Ticker(symbol)
    exchange_rate_USD = get_exchange_rate_USD()
    rt = {}
    rt['code'] = symbol
    rt['name'] = ticker.info.get('longName')
    rt['time'] = datetime.now().isoformat().split('T')[1][:8]
    rt['current_price'] = float(ticker.info.get('regularMarketPrice', 0)) * exchange_rate_USD
    rt['open_price'] = float(ticker.info.get('regularMarketOpen', 0)) * exchange_rate_USD
    rt['highest_price'] = float(ticker.info.get('regularMarketDayHigh', 0)) * exchange_rate_USD
    rt['lowest_price'] = float(ticker.info.get('regularMarketDayLow', 0)) * exchange_rate_USD
    rt['yesterday_price'] = float(ticker.info.get('regularMarketPreviousClose', 0)) * exchange_rate_USD
    rt['price_change'] = rt['current_price'] - rt['yesterday_price']
    rt['price_change_rate'] = (rt['price_change'] / rt['yesterday_price'] * 100) if rt['yesterday_price'] != 0 else 0
    return rt