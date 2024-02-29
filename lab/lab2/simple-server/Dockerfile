FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

WORKDIR /src
COPY requirements.txt .
COPY main.py .
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8501"]

EXPOSE 8501