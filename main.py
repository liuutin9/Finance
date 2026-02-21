from utils.get_stock_price import get_stock_price_tw, get_stock_price_us
from utils.stock_repo import update_stock_price, get_stocks

stocks = get_stocks()
for stock in stocks['TW']:
    stock_price_info = get_stock_price_tw(stock)
    update_stock_price("TW", stock, stock_price_info['current_price'], stock_price_info['yesterday_price'])
for stock in stocks['US']:
    stock_price_info = get_stock_price_us(stock)
    update_stock_price("US", stock, stock_price_info['current_price'], stock_price_info['yesterday_price'])