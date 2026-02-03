## This script generates a new django secret key and updates the .env file accordingly.
import os
import re
import secrets
import string

from pathlib import Path

# Get grandparent directory of the current file
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()


def generate_safe_secret_key(length=50):
    """
    Generate a Django-compatible secret key without problematic special characters.
    
    Excludes characters that can cause issues with:
    - Shell variable substitution: $ ! ` \
    - Docker Compose variable substitution: $
    - YAML parsing issues: : { } [ ] , & * # ? | - < > = ! % @ `
    
    Uses only alphanumeric characters and safe special characters: - _ + . ~
    This provides sufficient entropy while avoiding shell/Docker conflicts.
    
    Args:
        length: Length of the secret key (default: 50 characters)
        
    Returns:
        A secure random string safe for use in .env files
    """
    # Safe character set: alphanumeric + safe special characters
    # Excludes: $ ! ` \ : { } [ ] , & * # ? | < > = % @
    safe_chars = string.ascii_letters + string.digits + "-_+.~"

    # Generate cryptographically secure random string
    secret_key = "".join(secrets.choice(safe_chars) for _ in range(length))

    return secret_key


def generate_django_secret():
    # check if .env file exists in parent directory
    env_file = os.path.join(PROJECT_ROOT, ".env")
    if not os.path.exists(env_file):
        ## return error if it doesn't exist informing user to create one from .env.example
        print(
            f".env file not found at {env_file}. Please create one from .env.example before running this script."
        )
        return 1

    # Read the contents of the .env file
    with open(env_file, "r") as f:
        content = f.read()

    # Generate a new secret key (safe for shell/Docker)
    new_secret_key = generate_safe_secret_key()

    # Replace the old secret key with the new one
    content = re.sub(r"SECRET_KEY=(.*)", f"SECRET_KEY={new_secret_key}", content)

    # Write the updated content back to the .env file
    with open(env_file, "w") as f:
        f.write(content)

    print(f"New secret key generated and updated in {env_file} successfully.")
    print(f"Secret key length: {len(new_secret_key)} characters")
    print("Character set: alphanumeric + safe special characters (-_+.~)")


if __name__ == "__main__":
    generate_django_secret()
