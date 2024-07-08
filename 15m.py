from binance.client import Client
import pandas as pd
import time
import telegram
import requests

client = Client('YOUR_API_KEY', 'YOUR_API_SECRET')

bot = telegram.Bot(token='7069593892:AAGHGe8d4sQnMRPnVvFpM4NRoXOVQ4TUajg')
chat_id = '-1002241076003 ' 

exchange_info = client.futures_exchange_info()
usdt_m_symbols = [s['symbol'] for s in exchange_info['symbols'] if s['symbol'].endswith('USDT')]

print(usdt_m_symbols)


interval = Client.KLINE_INTERVAL_15MINUTE
limit = 21  

def check_volume_spike(symbol):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', *[f'ignore_{i}' for i in range(6)]])
    df['volume'] = pd.to_numeric(df['volume'])
    avg_volume = df['volume'].iloc[:-1].mean()  
    current_volume = df['volume'].iloc[-1]
  #  print(current_volume)
    return current_volume > 4 * avg_volume

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot7069593892:AAGHGe8d4sQnMRPnVvFpM4NRoXOVQ4TUajg/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()

while True:
    for symbol in usdt_m_symbols:
        if check_volume_spike(symbol):
            message = f"[{pd.Timestamp.now()}] {symbol} có volume khung 15m tăng đột biến!"
            send_message(-1002241076003 , message)
            print(message)
            # bot.sendMessage(chat_id=chat_id, text=message)

    time.sleep(15)