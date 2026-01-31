from fastapi import FastAPI
import joblib
import yfinance as yf
import pandas as pd
from pathlib import Path
import mlflow.sklearn


# MLflow設定
mlflow.set_tracking_uri("http://localhost:5000")

MODEL_NAME = "RMC_model"
MODEL_STAGE = "Production"

# サーバー起動時にモデルを一度だけ読み込む
# model_path = Path("models", "btc_prediction_model.pkl")
# model = joblib.load(model_path)
# API起動時に1回ロード
model = mlflow.sklearn.load_model(
    model_uri=f"models:/{MODEL_NAME}/{MODEL_STAGE}"
)


app = FastAPI()

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