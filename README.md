# manaql-ingest

## Installation

Prerequisites:
- python3
- uv

1. Create a virtual environment

`python3 -m venv .venv`

1. Activate the virtual environment

`source .venv/bin/activate`

1. Install the requirements

`pip install -r requirements.txt`

Added a dependency?
Run `pip3 freeze > requirements.txt`

## Running

1. Launch the "Run API" configuration in VSCode or run `cd src && uvicorn main:app --reload`
2. Execute requests against `http://localhost:8000/` or visit `http://localhost:8000/docs` for Swagger documentation
3. [Optional] Run via Docker:
- `docker build -t mtg-bulk-buy-server .`
- `docker run -p 8000:8000 mtg-bulk-buy-server`
