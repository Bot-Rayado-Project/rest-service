FROM python:3.10.2

WORKDIR /rest-service

COPY . .

RUN pip install poetry
RUN poetry install

CMD ["uvicorn" "main:app"]