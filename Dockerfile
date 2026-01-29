# 1. ベースとなるPython環境
FROM python:3.10-slim

# 2. 作業ディレクトリの作成
WORKDIR /app

# 3. 必要なファイルをコピー
COPY requirements.txt .
COPY scripts/main.py scripts/
COPY models/btc_prediction_model.pkl models/

# 4. ライブラリのインストール
RUN pip install -r requirements.txt
# RUN apt-get update && apt-get install -y git

# 5. APIサーバーの起動（0.0.0.0で公開）
# CMD ["python"]
CMD ["uvicorn", "scripts.main:app", "--host", "0.0.0.0", "--port", "10000"]