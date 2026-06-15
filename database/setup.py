"""
Sets up a remote Postgres database:
  1. Restart the Docker stack on the remote server
  2. Wait for Postgres to be ready
  3. Create the database
  4. Create tables and load data

Run with:  python setup.py
"""

import os
import subprocess
import sys
import time
from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load variables from the .env file into os.environ
load_dotenv()


# The folder where this script lives — used to find the SQL files
SCRIPT_DIR = Path(__file__).resolve().parent

# Path on the remote server where docker-compose.yml lives
PROJECT_DIR = "/home/centos/mini_project"

# file_path_name = SCRIPT_DIR / "REMOTE_USER"
# print(os.getenv(file_path_name))


# ---------------------------------------------------------------------------
# Step 1: Restart the remote Docker stack
# ---------------------------------------------------------------------------

def refresh_docker_stack():
    """Stop and restart the docker-compose stack on the remote server."""
    print("Refreshing remote Docker stack...")

    # Build the SSH target string, e.g. "centos@192.168.1.50"
    ssh_target = os.getenv("REMOTE_USER") + "@" + os.getenv("REMOTE_HOST")

    # Two commands to run on the remote server:
    #   - 'down -v' stops the containers and removes their data volumes
    #   - 'up -d'   starts them again in the background
    commands = [
        "cd " + PROJECT_DIR + " && sudo docker compose down -v",
        "cd " + PROJECT_DIR + " && sudo docker compose up -d",
    ]

    for cmd in commands:
        print("Running on remote:", cmd)

        # subprocess.run executes a command. We use the system 'ssh' program
        # to send our command to the remote server.
        result = subprocess.run(
            ["ssh", ssh_target, cmd],
            capture_output=True,
            text=True,
        )

        # A returncode of 0 means success. Anything else means it failed.
        if result.returncode != 0:
            print("Command failed:", result.stderr)
            return False

    return True


# ---------------------------------------------------------------------------
# Step 2: Wait for Postgres to be ready
# ---------------------------------------------------------------------------

def wait_for_postgres():
    """Try to connect to Postgres every second, up to 60 seconds."""
    print("Waiting for Postgres to be ready...")

    # We'll try for up to 60 seconds before giving up
    for attempt in range(60):
        try:
            # Try to open a connection. If Postgres isn't ready yet, this
            # will raise an error and we'll try again in a second.
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("DB_PORT"),
                dbname="postgres",
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
            )
            conn.close()
            print("Postgres is ready!")
            return True

        except psycopg2.OperationalError:
            # Not ready yet — wait a second and try again
            time.sleep(1)

    print("Postgres did not become ready in time.")
    return False

# ---------------------------------------------------------------------------
# Step 3: Create tables and load data
# ---------------------------------------------------------------------------

def load_schema_and_data():
    """Run 01_create_tables.sql and 02_insert_data.sql in our new DB."""
    print("Loading tables and data...")

    # Now we connect to the database we just created (from POSTGRES_DB)
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    cur = conn.cursor()

    # The two SQL files we want to run, in order
    sql_files = ["01_create_tables.sql", "02_insert_data.sql"]

    try:
        for filename in sql_files:
            print("Running", filename)
            sql_file = SCRIPT_DIR / filename
            sql = sql_file.read_text()
            cur.execute(sql)

        # Save all the changes to the database
        conn.commit()
        print("Tables and data loaded.")
    except Exception as e:
        # Something went wrong — undo everything we did in this session
        conn.rollback()
        print("Error loading schema/data:", e)
        raise
    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------------------------
# Main: run all the steps in order
# ---------------------------------------------------------------------------

def main():
    # Step 1: restart Docker. If it fails, stop here.
    if not refresh_docker_stack():
        print("Docker setup failed. Stopping.")
        return 1

    # Step 2: wait for Postgres. If it never starts, stop here.
    if not wait_for_postgres():
        return 1

    # Step 3: create tables and load data
    try:
        load_schema_and_data()
    except Exception as e:
        print("Database setup failed:", e)
        return 1

    print("\n--- Setup Complete ---")
    print("Postgres:", os.getenv("POSTGRES_HOST") + ":" + os.getenv("DB_PORT"))
    print("Adminer:  http://" + os.getenv("POSTGRES_HOST") + ":8080")
    return 0


# This runs main() only when the file is executed directly (not imported)
if __name__ == "__main__":
    sys.exit(main())