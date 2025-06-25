import os
import pandas as pd
from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# --- 설정 (app.py와 동일하게 유지) ---
load_dotenv()
VANNA_MODEL = 'gpt-4o-mini'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_CLIENT = QdrantClient(host=os.getenv("QDRANT_HOST"), port=os.getenv("QDRANT_PORT"))
if not OPENAI_API_KEY: raise ValueError("OpenAI API 키가 없습니다.")

class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

# --- Vanna 인스턴스 생성 및 DB 연결 ---
print("학습을 위한 Vanna 인스턴스 생성...")
config = {'model': VANNA_MODEL, 'api_key': OPENAI_API_KEY, 'client': QDRANT_CLIENT}
vn = MyVanna(config=config)
print(f"LLM(OpenAI: {VANNA_MODEL}) 및 Vector Store 설정 완료.")

try:
    vn.connect_to_postgres(
        host=os.getenv("POSTGRES_HOST"), port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DBNAME"), user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    print("PostgreSQL 데이터베이스 연결 완료.")
except Exception as e:
    print(f"DB 연결 중 오류 발생: {e}")
    exit()

# --- 모델 학습 ---
print("\n바나 모델 학습 시작...")
# (이전 코드의 모든 vn.train(...) 호출 코드를 여기에 붙여넣으시면 됩니다.)
sql_for_schema = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema IN ('humanresources', 'person', 'production', 'purchasing', 'sales')"
df_information_schema = vn.run_sql(sql_for_schema)
plan = vn.get_training_plan_generic(df_information_schema)
vn.train(plan=plan)
vn.train(documentation="The 'Human Resources' department is called '인사 부서' in Korean.")
vn.train(question="1980년 1월 1일 이후에 태어난 직원의 모든 정보를 보여주세요.", sql="SELECT * FROM humanresources.employee WHERE birthdate >= '1980-01-01'")
vn.train(question="1980년 1월 1일 이후에 태어난 직원의 모든 정보를 보여주세요.", sql="SELECT * FROM humanresources.employee WHERE birthdate >= '1980-01-01'")
vn.train(question="2010년 1월 1일 이후에 고용된 직원의 정보를 보여주세요.", sql="SELECT * FROM humanresources.employee WHERE hiredate >= '2010-01-01'")
vn.train(question="부서 ID가 6이고 교대 근무 ID가 1인 직원의 부서 이력 정보를 알려주세요.", sql="SELECT * FROM humanresources.employeedepartmenthistory WHERE departmentid = 6 AND shiftid = 1")
vn.train(question="유형이 '직원'인 사람들의 모든 인물 정보를 보여주세요.", sql="SELECT * FROM person.person WHERE persontype = 'EM'")
vn.train(question="단가가 30 이상인 구매 주문 상세 내역을 보여주세요.", sql="SELECT * FROM purchasing.purchaseorderdetail WHERE unitprice >= 30")
print("\n모든 학습이 완료되었습니다.")