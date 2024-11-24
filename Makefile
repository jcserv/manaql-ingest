setup:
	cd manaql && pipx install poetry && poetry install && pre-commit install

run:
	@source scripts/set-env.sh && python3 manaql/manage.py ingest

download:
	@source scripts/set-env.sh && python3 manaql/manage.py ingest --save-json --json-path=manaql/ingest/artifacts/all_cards.json

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
