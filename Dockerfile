FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false
ENV TZ=America/Sao_Paulo

WORKDIR app/

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 madr.app:app