import yfinance as yf
import pandas as pd
import ta
import requests

# Telegram Config
BOT_TOKEN = "8801278553:AAGmEogRLAq-uDq2m1kd0dHpDhZ-2fpCVRk"
CHAT_ID = "1391074551"

# Stocks List
stocks = [
    "RELIANCE.NS",
    "TATAMOTORS.NS",
    "NRBBEARING.NS",
    "SEAMEC.NS",
    "UPL.NS",
    "SBIN.NS",
    "TCS.NS"
]

results = []

for stock in stocks:
    try:
          print(f"Checking {stock}")

        df = yf.download(stock, period="6mo", interval="1d")

        if len(df) < 50:
            continue

        # MACD
        macd = ta.trend.MACD(df['Close'])
        df['macd'] = macd.macd()
        df['signal'] = macd.macd_signal()

        # Volume Average
        df['vol_avg'] = df['Volume'].rolling(20).mean()

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        # Conditions
        macd_cross = (
            prev['macd'] < prev['signal'] and
            latest['macd'] > latest['signal']
        )

        volume_breakout = latest['Volume'] > latest['vol_avg'] * 2

        consolidation_breakout = (
            latest['Close'] >= df['Close'].rolling(20).max().iloc[-1] * 0.98
        )

        if macd_cross and volume_breakout and consolidation_breakout:
            results.append(
                f"🚀 {stock}\n"
                f"Close: {round(float(latest['Close']),2)}\n"
                f"Volume Spike: YES\n"
                f"MACD Bullish: YES\n"
                f"Breakout Near: YES\n"
            )

    except Exception as e:
        print(stock, e)

# Final Message
if results:
    message = "📈 TOP STOCK ALERTS\n\n" + "\n----------------\n".join(results)
else:
    message = "No strong setups today."

# Send Telegram Message
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(url, data=payload)

print("Alert Sent")

