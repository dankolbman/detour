FROM python:3.7-alpine AS base

WORKDIR /usr/src/app

RUN apk update \
    && apk add --no-cache \
        postgresql-dev \
        postgresql-client \
        gcc \
        zlib-dev \
        jpeg-dev \
        libjpeg \
        python3-dev \
        musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "bin/entrypoint.sh" ]


FROM base AS dev_reqs

RUN pip install --no-cache-dir -r dev-requirements.txt
