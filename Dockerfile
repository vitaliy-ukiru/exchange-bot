FROM python:3.11-slim-buster as python-base
LABEL author = "ukiru" description="Telegram CBR Exchage Bot"


ENV POETRY_VERSION=1.5.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as app
RUN addgroup --system app && adduser --system --group app

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app
COPY ../poetry.lock pyproject.toml ./

RUN poetry check && \
    poetry install --no-interaction --no-cache --no-root


COPY .. .
USER app
ENTRYPOINT ["poetry", "run", "python", "-m", "exchangebot"]
CMD ["polling"]