from fastapi import FastAPI
import joblib
import yfinance as yf
import pandas as pd

app = FastAPI()

# サーバー起動時にモデルを一度だけ読み込む
model = joblib.load("models/btc_prediction_model.pkl")

@app.get("/")
def read_root():
    return {"message": "Bitcoin Prediction API is running!"}

@app.get("/predict")
def predict_next_day():
    # 最新データを取得して特徴量を作成
    print("download start")
    data = yf.download("BTC-USD", period="5d", interval="1d")
    print("download done")
    latest_return = data['Close'].pct_change().iloc[-1]
    latest_ma5 = (data['Close'] / data['Close'].rolling(window=5).mean()).iloc[-1]
    
    # 予測
    features = pd.DataFrame([[latest_return, latest_ma5]], columns=['Return', 'MA5'])
    prediction = model.predict(features)[0]
    
    return {
        "prediction": "Up" if prediction == 1 else "Down",
        "confidence_score": 0.85, # 例
        "timestamp": pd.Timestamp.now().isoformat()
    }