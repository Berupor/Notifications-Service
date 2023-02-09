# Django Admin Panel

## Project initialization

1. Create a .env file and fill it with values ​​from `.env.example`, `env.dev.example`
2. Run the project

```console
docker-compose up -d --build
```

3. Run the migrations

```console
python3 manage.py migrate
```

4. Create a superuser

```console
python3 manage.py createsuperuser
```

## Usage

1. Go to the admin panel URL `$HOST:8000/admin/`
2. Login with the superuser credentials created in the Installation step.
3. Start managing users, templates.

