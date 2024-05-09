# This Dockerfile is used for a deploy Heroku-style (not for development)

FROM python:3.12-slim-bookworm AS crates
ADD src/ src/
ADD Cargo.toml Cargo.toml
ADD Cargo.lock Cargo.lock
RUN apt update && \
    apt install -y curl build-essential curl && \
    curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    pip install maturin>=1.5.1 && \
    maturin build -o /wheels/

FROM python:3.12-slim-bookworm
ARG PORT
ADD poetry.lock poetry.lock
ADD pyproject.toml pyproject.toml
COPY --from=crates /wheels /wheels
RUN pip install poetry>=1.8.0 && \
    poetry install --no-dev && \
    poetry run pip install /wheels/*

ADD config.py config.py
ADD migrations/ migrations/
ADD whiskyton/ whiskyton/

CMD poetry run gunicorn --bind 0.0.0.0:$PORT whiskyton.wsgi:app
