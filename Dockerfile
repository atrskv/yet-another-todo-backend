FROM python:3.12-slim as todolist

WORKDIR /app

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./

RUN poetry install --only main --no-root

COPY . .

RUN pip install uvicorn

EXPOSE 8000
CMD ["uvicorn", "yet_another_todo.app:app", "--host", "0.0.0.0", "--port", "8000"]
