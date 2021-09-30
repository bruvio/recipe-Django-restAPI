# FROM python:3.8-slim

FROM python:3.8-alpine

MAINTAINER bruvio

ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"




COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN adduser -D user
USER user



# ENTRYPOINT [ "./run.sh" ]
