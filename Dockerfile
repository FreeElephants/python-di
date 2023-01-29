FROM python:3.11-alpine

# Begin dev dependencies

RUN pip install --upgrade pip \
    && pip install  \
        black \
        build \
        coverage \
        pylint \
        pylint-quotes \
        twin

# End dev dependencies

ENV HOME=/app

WORKDIR /app
# End project env
