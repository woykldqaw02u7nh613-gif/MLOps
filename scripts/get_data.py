import yfinance as yf

# 1. ティッカーシンボルを指定（ビットコイン: BTC-USD, Apple: AAPL など）
ticker = "BTC-USD"
data = yf.Ticker(ticker)

# 2. 履歴データの取得（期間: 1ヶ月, 間隔: 1日）
# period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
# interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
history = data.history(period="1mo", interval="1d")

# 3. 中身の確認
print(history.head())

# 4. CSVとして保存（ML用のデータセット作成）
history.to_csv("bitcoin_data.csv")