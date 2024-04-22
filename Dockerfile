FROM python:3.9-alpine3.13

LABEL maintainer="szymon.wais@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY /scripts /scripts


WORKDIR /app
EXPOSE 8000
EXPOSE 5000


RUN apk add --update --no-cache postgresql-client ffmpeg \
    && apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /requirements.txt \
    && apk del .tmp-deps \
    && adduser --disabled-password --no-create-home app \
    && mkdir -p /vol/web/static \
    && mkdir -p /vol/web/media \
    && chmod -R 755 /vol \
    && chown -R app:app /vol \
    && chmod -R +x /scripts


ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]


