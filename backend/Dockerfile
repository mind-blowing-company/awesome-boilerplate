FROM python:3.7.3-slim

RUN apt-get update
RUN apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
