.PHONY: setup test run download download-dry-run migrations migrate dev-db dev-db-down

UV_RUN := uv run --project manaql

setup:
	cd manaql && uv sync && uv run pre-commit install

test:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py test tests

download:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py download

ingest:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py ingest --file=scryfall_data.json

process:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py process

generate-embeddings:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py generate_embeddings --batch-size 50

run:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py all

schedule:
	fly machine run python:3.12-slim --vm-size shared-cpu-1x --vm-memory 1024 --schedule=daily --command "python manage.py all"

migrations:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py makemigrations database

migrate:
	@source scripts/set-env.sh && $(UV_RUN) python manaql/manage.py migrate database

dev-db:
	docker compose -p manaql -f docker-compose.yml up --detach

dev-db-down:
	docker compose -p manaql -f docker-compose.yml down -v

test-db:
	docker compose -p manaql-test -f docker-compose.test.yml up --detach

test-db-down:
	docker compose -p manaql-test -f docker-compose.test.yml down -v

gen-models:
	$(UV_RUN) datamodel-codegen --input schema.graphql --input-file-type graphql --output model.py
