FROM python:3.12
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# templates 폴더를 포함하여 프로젝트의 모든 파일을 복사합니다.
COPY . .

EXPOSE 8084
CMD ["gunicorn", "--bind", "0.0.0.0:8084", "--workers", "4", "-k", "gevent", "vanna_flask:server"]