# generates all secrets for project

from scripts.generate_django_secret import generate_django_secret
from scripts.generate_postgres_password import generate_postgres_password

generate_django_secret()
generate_postgres_password()