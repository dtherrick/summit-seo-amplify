#!/usr/bin/env python3

import secrets
import string
import uuid
from pathlib import Path
import subprocess
import argparse

def generate_password(length: int = 32) -> str:
    """Generate a secure password with mixed characters."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_secret_key() -> str:
    """Generate a secure secret key using OpenSSL."""
    try:
        result = subprocess.run(
            ['openssl', 'rand', '-hex', '32'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Fallback if openssl is not available
        return secrets.token_hex(32)

def main():
    parser = argparse.ArgumentParser(description='Generate secure environment values')
    parser.add_argument('--output', '-o', help='Output file for the secure values')
    args = parser.parse_args()

    # Generate secure values
    secure_values = {
        'SECRET_KEY': generate_secret_key(),
        'REDIS_PASSWORD': generate_password(32),
        'GRAFANA_ADMIN_PASSWORD': generate_password(24),
        'SMTP_PASSWORD': generate_password(24),
        'AWS_ACCESS_KEY_ID': f"AKIA{secrets.token_hex(8).upper()}",
        'AWS_SECRET_ACCESS_KEY': generate_password(40),
        'AWS_SESSION_TOKEN': generate_password(64),
        'POSTGRES_PASSWORD': generate_password(24),
    }

    # Print values
    print("\nGenerated secure values:")
    print("=" * 50)
    for key, value in secure_values.items():
        print(f"{key}={value}")
    print("=" * 50)

    # Save to file if specified
    if args.output:
        output_path = Path(args.output)
        with output_path.open('w') as f:
            for key, value in secure_values.items():
                f.write(f"{key}={value}\n")
        print(f"\nValues have been saved to {output_path}")

    print("\nIMPORTANT: Store these values securely and never commit them to version control!")

if __name__ == "__main__":
    main() 