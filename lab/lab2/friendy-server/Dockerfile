FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /src
COPY internal ./internal
COPY models ./models
COPY routers ./routers
COPY requirements.txt .
COPY main.py .
RUN apt-get update && apt install -y libmariadb-dev
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8501"]

EXPOSE 8501