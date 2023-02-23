FROM python:3.10-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP /opt/app/main.py

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install --no-install-recommends -y \
     curl \
     \
     && pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt \
     \
     && apt autoremove -y \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

COPY src/ /opt/app/

RUN groupadd -r api && useradd -d /opt/app -r -g api api \
     && chown api:api -R /opt/app

USER api

ENTRYPOINT gunicorn wsgi_app:app -w 4 --bind 0.0.0.0:5000
