
---

## 🔹 1. Install PostgreSQL

```bash
brew install postgresql
```

Start the service:

```bash
brew services start postgresql
```

Check version:

```bash
psql --version
```

---

## 🔹 2. Setup Database & User

1. Open Postgres shell:

   ```bash
   psql postgres
   ```

2. Create a new database user (with password):

   ```sql
   CREATE USER myuser WITH PASSWORD 'mypassword';
   ```

3. Create a database:

   ```sql
   CREATE DATABASE mydb OWNER myuser;
   ```

4. Give privileges:

   ```sql
   GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
   ```

Exit:

```sql
\q
```

---

## 🔹 3. Install Python PostgreSQL Adapter

Inside your Django project (with venv active):

```bash
pip install psycopg2-binary
```

(You can use `psycopg2` instead, but `-binary` is easier for local dev.)

---

## 🔹 4. Configure Django to Use PostgreSQL

In your project’s **`settings.py`**, update the `DATABASES` section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🔹 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔹 6. Test Connection

Run the dev server:

```bash
python manage.py runserver
```

If everything is configured, Django should connect to Postgres without issues.

---

## 🔹 7. (Optional but Recommended) Use Environment Variables

Instead of hardcoding DB credentials in `settings.py`, install `python-decouple`:

```bash
pip install python-decouple
```

Then in **`.env`**:

```
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
```

Update **`settings.py`**:

```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

---