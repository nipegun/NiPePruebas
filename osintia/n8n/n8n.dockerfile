FROM n8nio/n8n:latest

USER root
RUN apk add --no-cache docker su-exec \
    && adduser node root
RUN apk add \
    wget \
    git \
    gcc \
    make \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev
ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache python3 py3-pip py3-beautifulsoup4 py3-termcolor py3-httpx py3-trio py3-tqdm py3-requests
RUN git clone https://github.com/megadose/holehe.git /opt/holehe \
    && cd /opt/holehe \
    && python3 setup.py install
RUN apk add --no-cache py3-flask
USER node
COPY ./social-api.py /opt/social-api.py
