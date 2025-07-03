# app.py
import os

from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from vanna.flask import VannaFlaskApp

# -- 이 부분은 train.py와 동일하게 유지하여 같은 Vanna 설정을 사용합니다 --
# 1. 다중 상속을 사용하여 사용자 정의 Vanna 클래스 생성
class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config) # OpenAI_Chat의 초기화 메소드 호출

print("Vanna 인스턴스 생성 및 설정 (추론 모드)...")
config = {
    'model': 'gpt-4o-mini',
    'api_key': os.getenv("OPENAI_API_KEY"), # 공식 문서처럼 명시적으로 전달
    'client': QdrantClient(host=os.getenv("QDRANT_HOST"), port=os.getenv("QDRANT_PORT"))
}
vn = MyVanna(config=config)
print(f"LLM({vn.model}) 및 Vector Store 설정 완료.")

try:
    vn.connect_to_postgres(
        host= os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DBNAME", "Adventureworks"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD") # 사용자님의 postgres 비밀번호로 변경하세요.
    )
    print("PostgreSQL 데이터베이스 연결 완료.")
except Exception as e:
    print(f"DB 연결 중 오류 발생: {e}")
    exit()

app = VannaFlaskApp(vn,allow_llm_to_see_data=True)
app.run(host='0.0.0.0', port=8084)