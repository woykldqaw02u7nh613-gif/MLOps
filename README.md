# MLOps Bitcoin Prediction Project 🪙📈

**概要**

このリポジトリは、yfinance で取得したビットコイン（BTC-USD）の価格データを使って機械学習モデル（RandomForest）を学習し、MLflow で実験を管理、FastAPI で推論 API を提供するサンプル MLOps プロジェクトです。

---

## 🔧 必要条件

- **Python 3.10+**
- 依存パッケージのインストール:

```bash
pip install -r requirements.txt
```

---

## 📁 主要なディレクトリ/ファイル

- `scripts/` - データ取得、学習、API サーバーなどのスクリプト
  - `get_data.py` - サンプルデータのダウンロードと CSV 保存
  - `train.py` - 前処理、学習、MLflow ログ記録
  - `main.py` - FastAPI ベースの推論 API
- `data/` - データを保存するディレクトリ（例: `bitcoin_data.csv`）
- `models/` - 学習済みモデルを保存
- `mlruns/` - MLflow の実験ログ
- `Dockerfile` - コンテナ化のベース（※要編集: スクリプトを COPY するなど）
- `requirements.txt` - Python 依存関係

---

## 🚀 使い方

1. データの取得（任意）:

```bash
python scripts/get_data.py
# -> bitcoin_data.csv が作成されます
```

2. モデルの学習:

```bash
python scripts/train.py
```

- 実行中に MLflow にパラメータ、メトリクス、モデルが記録されます。
- MLflow UI を起動して結果を確認できます:

```bash
mlflow ui --backend-store-uri mlruns --port 5000
```

3. API サーバーを起動して推論を行う:

```bash
uvicorn scripts.main:app --reload --host 0.0.0.0 --port 8000
```

- 推論エンドポイント例:

```bash
curl http://localhost:8000/predict
```

---

## 🐳 Docker

- ビルドと実行:

```bash
docker build -t mlops-btc .
docker run -p 8000:10000 mlops-btc
```

> ⚠️ 注意: `Dockerfile` は現状で `scripts/` をコピーしていないため、コンテナ内で API を動かすには `Dockerfile` を編集（`COPY scripts/ scripts/` 等を追加）してください。

---

## ✨ 開発と貢献

- 変更や改善はプルリクを送ってください。簡単な説明と再現手順を添えてください。

---

## 📜 ライセンス

- MIT ライクな簡易ライセンスを想定しています。必要に応じて `LICENSE` ファイルを追加してください。

---

質問や追加してほしいドキュメントがあれば教えてください。✅
