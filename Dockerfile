FROM python:3.10.2

WORKDIR /rest-service

COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# sudo docker build -t rest .
# sudo docker run -p 8000:8000 --net host rest