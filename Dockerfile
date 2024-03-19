FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app

WORKDIR /home/app
RUN mkdir -p /home/app/database
COPY ./pyproject.toml ./poetry.lock* ./

# Install Poetry
RUN pip install poetry
RUN poetry install

COPY . /home/app

EXPOSE 8000

RUN poetry run python manage.py migrate

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
