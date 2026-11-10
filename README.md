# CK Realestate

Django application for the CK Realestate project.

## Requirements

- Python 3.12
- Git

## Local setup

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/ck-realestate.git
   cd ck-realestate
   ```

2. Create and activate a virtual environment.

   macOS:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env`.

5. Generate a local secret key and put it in `.env`:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. Initialize the database and create your local admin account:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Verify and run:

   ```bash
   python manage.py check
   python manage.py runserver
   ```

Visit http://127.0.0.1:8000/.
Admin login: http://127.0.0.1:8000/admin/.

## Daily development

Activate your virtual environment, then:

```bash
git switch main
git pull origin main
python -m pip install -r requirements.txt
python manage.py migrate
git switch -c feature/your-feature-name
python manage.py runserver
```

Commit your work on the feature branch and open a pull request into main.

## Database changes

After changing Django models:

```bash
python manage.py makemigrations
python manage.py migrate
```

Commit model changes and generated migration files together.
Each developer maintains their own local SQLite database.

## Dependency changes

After intentionally adding or updating a package:

```bash
python -m pip freeze > requirements.txt
```

Commit the updated requirements file.