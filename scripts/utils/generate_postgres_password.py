## Generates a password for the postgres user and puts it in the .env file.

import os
import re
import secrets

def generate_postgres_password():
    # check if .env file exists in parent directory
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.exists(env_file):
        ## return error if it doesn't exist informing user to create one from .env.example
        print(f".env file not found at {env_file}. Please create one from .env.example before running this script.")
        return 1

    # Read the contents of the .env file
    with open(env_file, 'r') as f:
        content = f.read()

    # Generate a new secure password
    new_password = secrets.token_urlsafe(16)

    # Replace the old POSTGRES_PASSWORD with the new one
    content = re.sub(r"DB_PASSWORD=(.*)", f"DB_PASSWORD={new_password}", content)

    # Write the updated content back to the .env file
    with open(env_file, 'w') as f:
        f.write(content)

    print(f"New Postgres password generated and updated in {env_file} successfully.")

if __name__ == "__main__":
    generate_postgres_password()