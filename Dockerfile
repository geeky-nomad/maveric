FROM python:3.11

WORKDIR /web/src

COPY ./requirements.txt /web/src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /web/src/requirements.txt

COPY ./modules/src/ /web/src
