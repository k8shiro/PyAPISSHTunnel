ARG PYTHON_VER

FROM python:3.7.3-alpine3.8

USER root
ARG proxy
ENV http_proxy ${proxy}
ENV https_proxy ${proxy}
ENV HTTP_PROXY ${proxy}
ENV HTTPS_PROXY ${proxy}

RUN mkdir src
WORKDIR src

RUN apk add --no-cache build-base libffi-dev openssl-dev
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apk add --update --no-cache netcat-openbsd openssh-client

CMD python -u ssh_tunnel.py
