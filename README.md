# 🤖 Movielens API
[![forthebadge made-with-python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-390/) [![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)


## ⭕ Contents
- [The project's purpose](#-the-project's-purpose)
- [What tools were used to create this project](#-what-tools-were-used-to-create-this-project)
- [Before you begin](#-before-you-begin)
- [how to run the project](#-how-to-run-the-project)
- [how to run tests](#-how-to-run-tests)
- [Final step](#-final-step)


## ⭕ The project's purpose
The purpose of this project is to leverage the [Movielens 20M Dataset](https://files.grouplens.org/datasets/movielens/ml-20m-README.html) from [Movielens](https://grouplens.org/datasets/movielens/) as its primary data source. It aims to provide a range of APIs for efficient data access and manipulation.


## ⭕ What tools were used to create this project
| Technology         |    🔗             |
| -----------------  | ----------------- |
| django v.5         | [[Github Link](https://github.com/django/django)] |
| django REST        | [[Github Link](https://github.com/encode/django-rest-framework)] |
| django-filter         | [[Github Link](https://github.com/carltongibson/django-filter)] |
| Simple JWT         | [[Github Link](https://github.com/jazzband/djangorestframework-simplejwt)] |
| drf-yasg           | [[Github Link](https://github.com/axnsan12/drf-yasg/tree/db42d356fb419a8fc334f2e369c1b721f27fc0b9)] |
| asyncio            | [[Github Link](https://github.com/python/cpython/blob/main/Doc/library/asyncio.rst) ] |
| pandas         | [[Github Link](https://github.com/pandas-dev/pandas)] |
| poetry             | [[Github Link](https://github.com/python-poetry/poetry)] |
| docker             | [[Github Link](https://github.com/docker-library/python)] |
| docker-compose     | [[Github Link](https://github.com/docker/compose)] |
| pytest             | [[Github Link](https://github.com/pytest-dev/pytest)] |
| coverage           | [[Github Link](https://github.com/nedbat/coveragepy?tab=readme-ov-file)] |
| mypy               | [[Github Link](https://github.com/python/mypy)] |


## ⭕ Before you begin
Before you begin, please follow these steps:

1. Create a folder named `datasets` in the `root` directory.
2. Download and extarct the [ml-20m](https://files.grouplens.org/datasets/movielens/ml-25m.zip) dataset in the `datasets` directory.

It should look like this:
```
├── datasets
│   └── ml-20m
│       ├── links.csv
│       ├── movies.csv
│       └── tags.csv
```

## ⭕ How to Run the Project
Navigate to the root of the project. <br>
To build the image from the Dockerfile, run:
```commandline
docker compose up --build -d
```

<br>Or, there's a `Makefile` for your convenience, so just run: (Check other commands too!)
```commandline
make run
```

<br>Now, you can check the **Swagger** URL for API documentation.
```commandline
http://127.0.0.1:8000/swagger/
```

<br>🌟 Now, you need to load the `ml-20m` dataset in to the database.
```commandline
make load_data
```

<br>Or, If you want to run the project locally, you need to have `poetry` installed first.
```commandline
pip install poetry
poetry install
poetry run python manage.py runserver 0.0.0.0:8000
poetry run python manage.py load_datasets
```

## ⭕ How to run tests
Run _pytest_ command to run the tests separately.<br>
```commandline
make tests
```

<br>And, what about Test Coverage?
```commandline
make coverage

# Backend Directory               Stmts   Miss  Cover
# -----------------------------------------------------
# Test Coverage TOTAL              255     30    88%
```

<br>🌟 This project has been thoroughly checked with `mypy` for type consistency, and it currently passes all mypy checks without any issues.
```commandline
make mypy
```

## ⭕ Final step
```commandline
make coffee
```
#### Be Happy Even if Things Aren’t Perfect Now. 🎉🎉🎉
#### Enjoy your coffee! ☕

![](https://i1.wp.com/justmaths.co.uk/wp-content/uploads/2016/10/celebration-gif.gif)
