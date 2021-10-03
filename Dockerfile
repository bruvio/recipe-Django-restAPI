FROM python:3.8-slim
# set up the psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client


ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/
RUN pip install psycopg2==2.8.3

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


RUN apt-get autoremove -y gcc

EXPOSE 8000
COPY . /code/
# ENTRYPOINT [ "./run.sh" ]
