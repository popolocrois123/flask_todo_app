from sqlalchemy import create_engine
# モデルが定義されているファイルをインポート
from app import Base, TODO_DB 

# エンジンの作成
engine = create_engine("sqlite:///todo.db")

# 1. 全テーブルを削除
Base.metadata.drop_all(engine)

# 2. モデル定義に基づき、全テーブルを再作成
Base.metadata.create_all(engine)

print("データベースをリセットしました。")