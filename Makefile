
coffee:
	@printf 'Be Happy Even if Things Aren’t Perfect Now. 🎉🎉🎉\n'
	@printf 'Enjoy your coffee! ☕\n'

dev:
	@docker compose -f docker-compose.yaml up --build

run:
	@docker compose -f docker-compose.yaml up --build -d

down:
	@docker compose -f ./docker-compose.yaml down --remove-orphans

load_data:
	@docker exec -it movielens_django poetry run python manage.py load_datasets

shell:
	@docker exec -it movielens_django bash

tests:
	@docker exec -it movielens_django poetry run pytest

coverage:
	@docker exec -it movielens_django poetry run coverage run -m pytest
	@docker exec -it movielens_django poetry run coverage report

mypy:
	@docker exec -it movielens_django poetry run mypy .

.PHONY: coffee dev run down load_data shell tests coverage mypy
