import requests
import urllib3

# Close SSL verification warnings to keep the terminal output clean
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        rt['price_change'] = float(data['z']) - float(data['y'])
        rt['price_change_rate'] = (rt['price_change'] / float(data['y'])) * 100 if float(data['y']) != 0 else 0
        return rt
    else:
        return f"Failed to fetch data for {symbol}"