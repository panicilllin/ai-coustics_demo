#
FROM python:3.10
WORKDIR /backend
COPY . /backend/
RUN pip install --upgrade pip  \
    && pip install --no-cache-dir --upgrade -r /backend/requirements.txt  \
    && apt-get -y update  \
    && apt-get -y upgrade  \
    && apt-get install -y sqlite3 libsqlite3-dev  \
    && mkdir -p /backend/logs  \
    && mkdir -p /backend/storage  \
    && mkdir -p /backend/tmp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]