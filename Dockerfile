FROM python:3.10-slim

# environment
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1 \
    URLLIB_VERSION=1.26.15


# create a directory and make it accessible to the user
RUN mkdir /app

# poetry
RUN pip install "poetry==$POETRY_VERSION" "urllib3==$URLLIB_VERSION"

# copy only requirements to cache them in docker layer
WORKDIR /app
COPY src/pyproject.toml /app/
# COPY src/poetry.loc[k] /app/

# project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi


COPY src/ /app/src/
COPY presets/ /app/presets/

ENV PYTHONPATH "${PYTHONPATH}:/app/src"
EXPOSE 8181

# run
WORKDIR /app/src/
CMD ["streamlit", "run", "Homepage.py", "--server.port", "8181", "--server.address", "0.0.0.0" , "--browser.gatherUsageStats", "False"]
