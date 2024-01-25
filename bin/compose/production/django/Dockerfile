FROM python:3.10.4                                                                                    
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD    ./bin/requirements .
RUN    apt-get update -y
RUN    pip install --upgrade pip
RUN    pip install -r production.txt

# Install NVM
RUN    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

# Activate NVM
RUN    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
RUN    . ~/.bashrc

# Install Node.js 14.15.0
RUN    bash -l -c "nvm install 14.15.0"


COPY ./bin/compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./bin/compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./bin/compose/local/django/celery/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


# copy application code to WORKDIR
ADD ./{{ your_project_name }} /app

ENTRYPOINT ["/entrypoint"]
