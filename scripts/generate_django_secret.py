## This script generates a new django secret key and updates the .env file accordingly.
import os
import re

from django.core.management.utils import get_random_secret_key


def generate_django_secret():
    # check if .env file exists in parent directory
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.exists(env_file):
        ## return error if it doesn't exist informing user to create one from .env.example
        print(f".env file not found at {env_file}. Please create one from .env.example before running this script.")
        return 1

    # Read the contents of the .env file
    with open(env_file, 'r') as f:
        content = f.read()

    # Generate a new secret key
    new_secret_key = get_random_secret_key()

    # Replace the old secret key with the new one
    content = re.sub(r"SECRET_KEY=(.*)", f"SECRET_KEY={new_secret_key}", content)

    # Write the updated content back to the .env file
    with open(env_file, 'w') as f:
        f.write(content)

    print(f"New secret key generated and updated in {env_file}  successfully.")
    
if __name__ == "__main__":
    generate_django_secret()