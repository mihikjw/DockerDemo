FROM ubuntu
WORKDIR /code

RUN apt update && apt install python3 python3-pip uwsgi -y

COPY api/ api/

COPY api_schema.yml .
COPY main.py .
COPY Makefile .
COPY requirements.txt .
COPY uwsgi.ini .

RUN make

RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

CMD ["uwsgi", "--ini", "/code/uwsgi.ini"]