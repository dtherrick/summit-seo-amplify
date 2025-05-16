#!/usr/bin/env python3

import argparse
import os
import subprocess
from pathlib import Path

def run_command(command: str) -> None:
    """Run a shell command and print output."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        if e.output:
            print(e.output)
        if e.stderr:
            print(e.stderr)
        raise

def create_migration(message: str) -> None:
    """Create a new migration with autogenerate."""
    command = f"alembic revision --autogenerate -m {message}"
    run_command(command)

def upgrade(revision: str = "head") -> None:
    """Upgrade database to a specified revision."""
    command = f"alembic upgrade {revision}"
    run_command(command)

def downgrade(revision: str) -> None:
    """Downgrade database to a specified revision."""
    command = f"alembic downgrade {revision}"
    run_command(command)

def show_history() -> None:
    """Show migration history."""
    command = "alembic history"
    run_command(command)

def show_current() -> None:
    """Show current revision."""
    command = "alembic current"
    run_command(command)

def main():
    parser = argparse.ArgumentParser(description="Manage database migrations")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create migration
    create_parser = subparsers.add_parser("create", help="Create a new migration")
    create_parser.add_argument("message", help="Migration message")

    # Upgrade
    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade database")
    upgrade_parser.add_argument("--revision", default="head", help="Target revision (default: head)")

    # Downgrade
    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade database")
    downgrade_parser.add_argument("revision", help="Target revision")

    # History
    subparsers.add_parser("history", help="Show migration history")

    # Current
    subparsers.add_parser("current", help="Show current revision")

    args = parser.parse_args()

    try:
        if args.command == "create":
            create_migration(args.message)
        elif args.command == "upgrade":
            upgrade(args.revision)
        elif args.command == "downgrade":
            downgrade(args.revision)
        elif args.command == "history":
            show_history()
        elif args.command == "current":
            show_current()
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main() 