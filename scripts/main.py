from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# リクエストボディの定義
class Item(BaseModel):
    name: str
    price: float
    description: str = None

# 文字列を保存するリクエスト
class TextData(BaseModel):
    text: str

# GET エンドポイント
@app.get("/")
def read_root():
    return {"message": "FastAPI へようこそ!"}

# 文字列を保存するエンドポイント
@app.post("/save/")
def save_text(data: TextData):
    try:
        # タイムスタンプ付きファイル名を作成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"saved_text_{timestamp}.txt"
        
        # ファイルに保存
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data.text)
        
        return {"status": "成功", "filename": filename, "message": "テキストを保存しました"}
    except Exception as e:
        return {"status": "エラー", "message": str(e)}

# # パスパラメータを使うエンドポイント
# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}

# # クエリパラメータを使うエンドポイント
# @app.get("/users/")
# def read_users(skip: int = 0, limit: int = 10):
#     return {"skip": skip, "limit": limit}

# # POST エンドポイント
# @app.post("/items/")
# def create_item(item: Item):
#     return {"name": item.name, "price": item.price, "description": item.description}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
