# FROM python:3.8-slim

FROM python:3.8-alpine

MAINTAINER bruvio

ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /code
WORKDIR /code


COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser -D user
USER user



COPY . /code/
ENTRYPOINT [ "./run.sh" ]
