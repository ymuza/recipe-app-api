#FROM devopspurplelab/python3.11-alpine-3.17
#LABEL maintainer="test.com"
#
#ENV PYTHONNUNBUFFERED 1
#
#
## Copies requirements to another folder
#COPY ./requirements.txt /tmp/requirements.txt
#COPY ./app /app
#WORKDIR /app
#EXPOSE 8000
#
#
#RUN python -m venv /py&& \  # creates a new virtual environment \
#    /py/bin/pip install --upgrade pip && \  # specify full python package inside env\
#    /py/bin/pip install -r /tmp/requirements.txt && \  # install list of requirements inside docker image\
#    rm -rf /tmp && \  # we dont want any extra files on the image\
#    adduser \  # adds a new user inside the image, so we don't have to use the root user\
#        --disabled-password \
#        --no-create-home \
#    django-user
#
#ENV PATH="/py/bin:$PATH"
#
#
## specifies the user we are switching for\
#USER django-user


FROM python:3.12

LABEL maintainer="test.com"

ENV PYTHONUNBUFFERED 1

# Copies requirements to another folder
COPY ./pyproject.toml ./poetry.lock /app/
WORKDIR /app
EXPOSE 8000

# Install curl
RUN apt-get update && \
    apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -


## Install project dependencies using Poetry
#RUN poetry config virtualenvs.create false && \
#    poetry install --no-root --no-interaction --no-ansi

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

## Remove unnecessary files
#RUN apk del curl

# Remove curl to keep the image clean and small
RUN apt-get remove --purge -y curl && apt-get autoremove -y && apt-get clean

# Set the default user
USER django-user







