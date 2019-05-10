ARG PYTHON_VER

FROM python:${PYTHON_VER}

USER root
ARG proxy
ENV http_proxy ${proxy}
ENV https_proxy ${proxy}
ENV HTTP_PROXY ${proxy}
ENV HTTPS_PROXY ${proxy}

RUN mkdir src

WORKDIR src

COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt


