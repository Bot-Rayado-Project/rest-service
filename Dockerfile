FROM python:3.10.2

WORKDIR /rest-service

COPY . .

RUN pip install -r requrements.txt

CMD ["uvicorn", "main:app"]