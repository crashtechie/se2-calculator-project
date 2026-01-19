## INITIAL ENVIRONMENT SETUP
    install UV: https://docs.astral.sh/uv/getting-started/installation/
    install Python 3.13 using uv: https://docs.astral.sh/uv/guides/install-python/
    initialize a new uv environment: 
    ```uv init .
    ```
    validate uv python version:
    ```uv run python --version
    ```
    install django:
    ```pip install django
    ```
    verify django installation:
    ```django-admin --version
    ```

## Setup environment variables
    copy the .env.example to .env file:
    ```cp .env.example .env
    ```
    run the following command to set the secret key and the postgres password in the .env file:
    ```uv run python scripts.secrets_gen
    ```

## start postgres docker container
    run the following command to start the postgres docker container:
    ```docker compose up -d
    ```

## Validate django server runs
    run the development server:
    ```uv run python manage.py runserver
    ```
    open browser and navigate to http://localhost:8000 to see initial homepage.

