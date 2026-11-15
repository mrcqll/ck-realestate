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
## Realtor login (User Story #7)

The public homepage remains available without signing in. Follow **Realtor Login**
from the homepage or visit `/admin/login/`. Successful login opens the existing
Django administration area at `/admin/`; safe local `next` destinations are also
supported. Use the admin's **Log out** button to end the session (CSRF-protected
POST only).

Realtors use Django's existing user model. An account must be both **Active**
(`is_active`) and **Staff status** (`is_staff`) to sign in to administration.
Staff access does not grant model permissions: assign only the required permissions
or groups in the existing Users administration page. Authenticated non-staff users
receive HTTP 403 from administrative pages and actions.

To bootstrap an administrator, activate the virtual environment and run:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Enter credentials interactively; do not commit or share them. Sign in with that
account, open **Authentication and Authorization → Users**, and create or select
the Realtor account. Enable **Active** and **Staff status**, assign the required
permissions, and save. Reserve superuser access for trusted administrators.
There is no public account registration. This story adds no models or migrations.

Settings now load `.env` using the existing `python-dotenv` dependency:

- `DJANGO_SECRET_KEY`: a privately generated secret key, required at startup.
- `DJANGO_DEBUG=True`: local HTTP development; set `False` for production.
- `DJANGO_ALLOWED_HOSTS`: comma-separated permitted hostnames.

With debug disabled, session and CSRF cookies require HTTPS. Serve production over
HTTPS and configure TLS redirects at the hosting layer. Session cookies remain
HTTP-only; session and CSRF cookies use SameSite=Lax. Configure proxy trust only
for your actual deployment. Do not use the example secret in production.

Run the focused authentication tests and configuration checks:

```bash
python manage.py test
python manage.py check
```

The current application has no property models or browsing pages beyond the
public homepage. The tests exercise the existing admin user/group management
pages, direct GET/POST access, staff model permissions, generic authentication
failures, redirects, CSRF, logout, and public homepage access. Future property
models should be registered with the existing admin to inherit these protections.
