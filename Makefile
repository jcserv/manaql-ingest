.PHONY: setup test run download download-dry-run migrations migrate dev-db dev-db-down

setup:
	cd manaql && pipx install poetry && poetry install && pre-commit install

test:
	@source scripts/set-env.sh && python3 manaql/manage.py test tests

run:
	@source scripts/set-env.sh && python3 manaql/manage.py ingest --file=all_cards.json

run-failed:
	@source scripts/set-env.sh && python3 manaql/manage.py ingest --file=failed_scryfall_cards.json

download:
	@source scripts/set-env.sh && python3 manaql/manage.py download --file=all_cards.json

download-dry-run:
	@source scripts/set-env.sh && python3 manaql/manage.py download --dry-run

migrations:
	@source scripts/set-env.sh && python3 manaql/manage.py makemigrations database

migrate:
	@source scripts/set-env.sh && python3 manaql/manage.py migrate database

dev-db:
	docker compose -p manaql -f docker-compose.yml up --detach

dev-db-down:
	docker compose -p manaql -f docker-compose.yml down -v

test-db:
	docker compose -p manaql-test -f docker-compose.test.yml up --detach

test-db-down:
	docker compose -p manaql-test -f docker-compose.test.yml down -v

gen-models:
	datamodel-codegen --input schema.graphql --input-file-type graphql --output model.py
