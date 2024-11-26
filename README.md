# manaql-ingest

![visitors](https://img.shields.io/endpoint?url=https://vu-mi.com/api/v1/views?id=jcserv/manaql-ingest)

manaql-ingest is a Django application that ingests Scryfall card data into a PostgreSQL database, to be used by [manaql-api](https://github.com/jcserv/manaql) project.

## installation

### prerequisites
- python3
- pipx
- poetry

### running locally
1. Create a virtual environment
`python3 -m venv .venv`

2. Activate the virtual environment
`source .venv/bin/activate`

3. Run `make setup`
4. Run `poetry install`
5. Run `make download` to download the Scryfall data
6. Run `make ingest` to ingest the Scryfall data into the database
7. Run `make run` to process the Scryfall data into the card/printings tables
