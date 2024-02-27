FROM python:3.10.6
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD    ./bin/requirements ./requirements
RUN    apt-get update -y && apt-get install -y vim
RUN    pip install --upgrade pip
RUN    pip install -r ./requirements/local.txt

COPY ./bin/compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./bin/compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./bin/compose/local/django/celery/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


ENTRYPOINT ["/entrypoint"]
