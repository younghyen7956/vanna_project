from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from service.vanna_service_impl import VannaServiceImpl

VannaRouter = APIRouter()

def injectService() -> VannaServiceImpl:
    return VannaServiceImpl.getInstance()


# POST 요청의 body 형식을 정의하는 모델
class AskRequest(BaseModel):
    question: str

@VannaRouter.post("/ask",
                  summary="자연어로 명령어를 하면 Sql문으로 변환 후 결과를 출력합니다.",
                  description="JSON 본문에 담긴 자연어 질문을 받아 SQL 생성, 실행, 차트 생성을 한번에 처리합니다."
                  )
async def ask(question: str = Query(...),
    VannaService: VannaServiceImpl = Depends(injectService)):
    try:
        # Service로부터 원본 객체들이 담긴 딕셔너리를 받습니다.
        service_result = VannaService.ask_vanna(question)

        # --- [핵심] 여기서만 객체를 다루고 JSON으로 변환합니다. ---
        df = service_result.get("dataframe")
        # print(f"🚨 [DEBUG-Controller] Service로부터 받은 df 타입: {type(df)}")
        # print(f"    df 내용(일부): {str(df)[:200]}...")  # 내용도 일부 확인
        sql = service_result.get("sql")
        model_name = service_result.get("model")
        fig = service_result.get("fig")

        # 1. 원본 DataFrame 객체를 확인합니다. (이때 .empty를 사용)
        results_json = []
        if df is not None and not df.empty:
            # 2. JSON으로 변환합니다.
            results_json = df.to_dict('records')

        # 1. 원본 Figure 객체를 확인합니다.
        chart_json = None
        if fig is not None:
            # 2. JSON으로 변환합니다.
            chart_json = fig.to_json()

        # 3. 최종적으로 변환된 데이터만 클라이언트에게 보냅니다.
        return {
            "question": question,
            "model": model_name,
            "sql": sql,
            "results": results_json,
            "chart_json": chart_json
        }
    except Exception as e:
        # 간단하게 모든 예외를 500으로 처리, 필요시 세분화 가능
        raise HTTPException(status_code=500, detail=str(e))