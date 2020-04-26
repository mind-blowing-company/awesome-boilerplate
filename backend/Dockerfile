FROM python:3.7.3-slim

# RUN apt-get update
# RUN apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt ./
RUN \
 pip install -U pip --no-cache-dir &&\
 pip install -r requirements.txt --no-cache-dir &&\
 chown 1000:1000 -R /app

COPY --chown=1000:1000 . ./
USER 1000

EXPOSE 8000
ENTRYPOINT [ "uvicorn" ]
CMD ["main:app", "--host", "0.0.0.0"]
