# vanna_flask.py (가장 간단한 기본 UI 버전)

import os
from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from vanna.flask import VannaFlaskApp
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# Vanna와 데이터베이스 연결을 위한 사용자 정의 클래스
class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

print("Vanna 인스턴스 생성 및 설정...")
# 환경 변수에서 설정을 읽어옵니다.
config = {
    'model': 'gpt-4o-mini',
    'api_key': os.getenv("OPENAI_API_KEY"),
    'client': QdrantClient(host=os.getenv("QDRANT_HOST"), port=int(os.getenv("QDRANT_PORT", "6333")))
}
vn = MyVanna(config=config)
print("Vanna 인스턴스 생성 완료.")

# PostgreSQL 데이터베이스에 연결합니다.
try:
    vn.connect_to_postgres(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DBNAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    print("PostgreSQL 데이터베이스 연결 완료.")
except Exception as e:
    print(f"DB 연결 중 오류 발생: {e}")
    exit()

# [수정된 부분]
# 커스텀 UI 관련 코드를 모두 제거하고, VannaFlaskApp 객체만 생성합니다.
print("Flask 앱 객체 생성...")
app = VannaFlaskApp(vn)

# Gunicorn이 직접 실행할 수 있도록, VannaFlaskApp 객체 안의
# 실제 Flask 앱을 'server' 변수에 할당합니다.
server = app.flask_app

print("애플리케이션 로딩 완료. 서버가 시작됩니다.")