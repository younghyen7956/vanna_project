import os
import pandas as pd
from vanna.openai import OpenAI_Chat
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv


# 부모 클래스가 있다고 가정합니다.
class vannaRepository:
    def ask(self, query: str):
        raise NotImplementedError


class vannaRepositoryImpl(vannaRepository):
    __instance = None
    load_dotenv()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.model_name = 'gpt-4o-mini'
        self.vn_openai = None
        self.get_DB_openai()
        print("--- vannaRepositoryImpl: __init__ 최초 초기화 완료 ---")

    def get_DB_openai(self):
        class VannaOpenAI(Qdrant_VectorStore, OpenAI_Chat):
            def __init__(self, config=None):
                Qdrant_VectorStore.__init__(self, config=config)
                OpenAI_Chat.__init__(self, config=config)

        qdrant_client = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=os.getenv("QDRANT_PORT", 6333))
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            print("경고: OPENAI_API_KEY가 설정되지 않았습니다.")
        else:
            self.vn_openai = VannaOpenAI(
                config={'model': self.model_name, 'api_key': openai_api_key, 'client': qdrant_client})
            try:
                # 접속에 사용할 변수들을 미리 정의합니다.
                host = os.getenv("POSTGRES_HOST", "localhost")
                port = os.getenv("POSTGRES_PORT", "5432")
                dbname = os.getenv("POSTGRES_DBNAME", "Adventureworks")
                user = os.getenv("POSTGRES_USER", "postgres")
                password = os.getenv("POSTGRES_PASSWORD")

                self.vn_openai.connect_to_postgres(
                    host=host,
                    port=port,
                    dbname=dbname,
                    user=user,
                    password=password
                )

                # [로그 추가] 성공적으로 연결된 DB 정보를 터미널에 출력합니다.
                print("✅ OpenAI Vanna 인스턴스 준비 완료.")
                print("-----------------------------------------------------")
                print("  🔌 연결된 PostgreSQL 데이터베이스 정보")
                print(f"  - Host: {host}")
                print(f"  - Port: {port}")
                print(f"  - Database: {dbname}")
                print(f"  - User: {user}")
                print("-----------------------------------------------------")

            except Exception as e:
                self.vn_openai = None
                print(f"DB 연결 실패: {e}")

    def ask(self, question: str) -> dict:
        if not self.vn_openai:
            raise ConnectionError("Vanna 서비스에 연결할 수 없습니다.")

        try:
            result_tuple = self.vn_openai.ask(question=question, allow_llm_to_see_data=True)

            if result_tuple is None:
                raise ValueError("Vanna가 DB에서 결과를 가져오는 데 실패했습니다.")

            df, sql, fig = (None, None, None)

            # [핵심] 반환된 튜플의 실제 순서에 맞게 변수를 할당합니다.
            if len(result_tuple) >= 2:
                sql = result_tuple[0]  # 첫 번째 값("SELECT...")을 sql 변수에 할당
                df = result_tuple[1]  # 두 번째 값(DataFrame)을 df 변수에 할당
            if len(result_tuple) >= 3:
                fig = result_tuple[2]  # 세 번째 값(Figure)을 fig 변수에 할당

            # 이제 각 변수에는 올바른 데이터가 담겨있습니다.
            return {
                "dataframe": df,
                "sql": sql,
                "fig": fig,
                "model": self.model_name,
            }
        except Exception as e:
            print(f"ask 처리 중 오류 발생: {e}")
            raise