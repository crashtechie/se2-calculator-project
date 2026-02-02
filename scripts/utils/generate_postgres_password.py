## Generates a password for the postgres user and puts it in the .env file.

import os
import re
import secrets
import string

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

def generate_safe_password(length=24):
    """
    Generate a secure password safe for use in .env files and Docker Compose.
    
    Uses only alphanumeric characters and safe special characters: - _ + . ~
    This avoids issues with shell/Docker variable substitution while maintaining
    high entropy for security.
    
    Args:
        length: Length of the password (default: 24 characters)
        
    Returns:
        A secure random password string
    """
    # Safe character set: alphanumeric + safe special characters
    safe_chars = string.ascii_letters + string.digits + '-_+.~'
    
    # Generate cryptographically secure random password
    password = ''.join(secrets.choice(safe_chars) for _ in range(length))
    
    return password

def generate_postgres_password():
    # check if .env file exists in parent directory
    env_file = os.path.join(PROJECT_ROOT, '.env')
    if not os.path.exists(env_file):
        ## return error if it doesn't exist informing user to create one from .env.example
        print(f".env file not found at {env_file}. Please create one from .env.example before running this script.")
        return 1

    # Read the contents of the .env file
    with open(env_file, 'r') as f:
        content = f.read()

    # Generate a new secure password (safe for shell/Docker)
    new_password = generate_safe_password()

    # Replace the old DB_PASSWORD with the new one
    content = re.sub(r"DB_PASSWORD=(.*)", f"DB_PASSWORD={new_password}", content)

    # Write the updated content back to the .env file
    with open(env_file, 'w') as f:
        f.write(content)

    print(f"New Postgres password generated and updated in {env_file} successfully.")
    print(f"Password length: {len(new_password)} characters")
    print(f"Character set: alphanumeric + safe special characters (-_+.~)")

if __name__ == "__main__":
    generate_postgres_password()