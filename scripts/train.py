import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib
import yfinance as yf
import pandas as pd
import datetime
from pathlib import Path


# --- 1. データ取得 (Data Ingestion) ---
print("データを取得中...")
ticker = "BTC-USD"
# 過去2年分のデータを取得
data = yf.download(ticker, period="2y", interval="1d")

# --- 2. 前処理 (Preprocessing / Feature Engineering) ---
print("前処理を実行中...")
df = data.copy()
# 特徴量1: 終値の変化率
df['Return'] = df['Close'].pct_change()
# 特徴量2: 5日間の移動平均乖離率
df['MA5'] = df['Close'] / df['Close'].rolling(window=5).mean()
# ターゲット: 翌日の終値が今日より高ければ1 (上昇), そうでなければ0
df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# 欠損値（NaN）を削除して、必要な列だけ抽出
df = df.dropna()
features = ['Return', 'MA5']
X = df[features]
y = df['Target']

# --- 3. モデル学習 (Model Training) ---
print("モデルを学習中...")
# 時系列データなので shuffle=False (過去データで学習し、未来データでテスト)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- 4. 評価 (Evaluation) ---
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"モデルの精度: {acc:.2%}")

# --- 5. モデル保存 (Model Storage) ---
model_filename = Path("models", "btc_prediction_model.pkl")
# model_filename = Path("models", f"btc_prediction_model_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl")
joblib.dump(model, model_filename)
print(f"モデルを保存しました: {model_filename}")

# --- 6. 予測 (Inference / Prediction) ---
# 最新（今日）のデータを使って、明日を予測してみる
latest_data = X.tail(1)
prediction = model.predict(latest_data)
result = "上昇 🚀" if prediction[0] == 1 else "下落 📉"
print(f"【予測】明日のビットコイン価格予測は... {result} です！")


# 1. 実験の名前を設定（バラバラにならないように管理）
mlflow.set_experiment("BTC_Prediction_Project")

with mlflow.start_run():
    # --- パラメータの設定 ---
    n_estimators = 100
    random_state = 42
    
    # --- パラメータを記録 ---
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("random_state", random_state)

    # モデル学習（前回のコードの続き）
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)

    # --- 精度を記録 (Metric) ---
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", acc)
    print(f"精度: {acc}")

    # --- モデルそのものを記録 (Artifact) ---
    mlflow.sklearn.log_model(model, "model")
    
    print("MLflowへの記録が完了しました！")