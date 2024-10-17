import subprocess
import sys

def run_command(command, description):
    print(f"Running {description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"{description} failed.")
        sys.exit(result.returncode)
    else:
        print(f"{description} completed successfully.")

def main():

    run_command("poetry run ruff check .", "Ruff")
    run_command("poetry run mypy .", "Mypy")

    run_command("poetry run python manage.py makemigrations", "Database makemigrations")
    run_command("poetry run python manage.py migrate", "Database Migration")

    run_command("poetry run pytest", "Pytest")

    run_command("poetry run python manage.py runserver", "Django Server")

if __name__ == "__main__":
    main()
