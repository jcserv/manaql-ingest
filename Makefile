setup:
	pre-commit install

run:
	python manage.py runserver

migrations:
	@source scripts/set-env.sh && python3 manage.py makemigrations

migrate:
	@source scripts/set-env.sh && python3 manage.py migrate

dev-db:
	docker compose -p manaql -f docker-compose.yml up --detach

dev-db-down:
	docker compose -p manaql -f docker-compose.yml down -v

test-db:
	docker compose -p manaql-test -f docker-compose.test.yml up --detach

test-db-down:
	docker compose -p manaql-test -f docker-compose.test.yml down -v
