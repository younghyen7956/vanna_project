# fastapi_app/Dockerfile

# 1. 파이썬 공식 이미지를 기반으로 시작합니다.
FROM python:3.12

# 2. 컨테이너 안의 작업 폴더를 /app 으로 설정
WORKDIR /app

# 3. [핵심] PYTHONPATH 환경 변수 설정
ENV PYTHONPATH=/app

# 4. requirements.txt 파일을 먼저 복사
#    빌드 컨텍스트가 fastapi_project 폴더이므로, 그 안의 requirements.txt를 복사합니다.
COPY requirements.txt ./

# 5. 필요한 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. fastapi_project 폴더의 모든 내용을 컨테이너의 /app 폴더 안으로 복사
COPY . .

# 7. 8000번 포트 개방
EXPOSE 8000

# 6. 8000번 포트를 외부에 개방하도록 설정합니다.
EXPOSE 8000

# 7. 컨테이너가 시작될 때 실행할 명령어를 정의합니다.
# uvicorn 서버를 실행하여 main.py 파일 안의 app 객체를 실행합니다.
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]