FROM python:3.10

WORKDIR /rest-service

COPY . .

RUN poetry install

CMD ["uvicorn" "main:app"]