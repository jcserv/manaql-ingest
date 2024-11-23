import os


class Config:
    def __init__(self):
        self.django_secret_key = os.getenv("DJANGO_SECRET_KEY")
        self.database = os.getenv("POSTGRES_DB")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.db_port = os.getenv("POSTGRES_PORT")

    def validate(self):
        if not self.django_secret_key:
            raise Exception("DJANGO_SECRET_KEY is not set")
        if not self.database:
            raise Exception("POSTGRES_DB is not set")
        if not self.user:
            raise Exception("POSTGRES_USER is not set")
        if not self.password:
            raise Exception("POSTGRES_PASSWORD is not set")
        if not self.host:
            raise Exception("POSTGRES_HOST is not set")
        if not self.db_port:
            raise Exception("POSTGRES_PORT is not set")
