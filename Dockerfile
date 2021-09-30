FROM python:3.8-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src/app


COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt




COPY . .
RUN pytest

