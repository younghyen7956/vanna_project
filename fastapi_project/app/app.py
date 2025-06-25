import os
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from controller.vanna_controller import VannaRouter
from repository.vanna_repository_impl import vannaRepositoryImpl

load_dotenv()
app = FastAPI(debug=True)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(VannaRouter)


@app.on_event("startup")
async def on_startup():
    repo = vannaRepositoryImpl.getInstance()
    # (원한다면 임베딩 캐시나 인덱스 로드도 이곳에서)
    print("✅ Startup: model checked.")  # 메시지 약간 수정


if __name__ == "__main__":
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 8080))
    uvicorn.run(app, host=host, port=port, log_level="debug")