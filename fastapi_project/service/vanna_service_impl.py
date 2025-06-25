from fastapi import UploadFile

from service.vanna_service import VannaService
from repository.vanna_repository_impl import vannaRepositoryImpl


# RAGService 인터페이스가 있다면 그것을 상속, 없다면 object 상속
class VannaServiceImpl(VannaService):
    __instance = None

    def __new__(cls, *args, **kwargs): # 싱글턴 인수 처리
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            # __init__에서 repo 초기화
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized_service'): # 서비스 초기화 플래그
            print("--- RAGServiceImpl: __init__ 최초 초기화 ---")
            self.vanna_repository = vannaRepositoryImpl.getInstance() # 레포지토리 인스턴스 생성 및 저장
        else:
            print("--- RAGServiceImpl: __init__ (이미 초기화됨) ---")


    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls() # __new__ 와 __init__ 호출
        return cls.__instance

    def ask_vanna(self, query: str) -> dict:
        """
        [수정] 질문을 받아 SQL, 데이터 결과, 차트 객체를 포함한 딕셔너리를 반환합니다.
        """
        if not query or not isinstance(query, str):
            raise ValueError("질문은 비어있지 않은 문자열이어야 합니다.")

        # Repository를 호출하고 결과를 딕셔너리로 받습니다.
        repo_result = self.vanna_repository.ask(query)
        # print(f"✅ [DEBUG-Service] Repository로부터 받은 df 타입: {type(repo_result.get('dataframe'))}")
        return repo_result

