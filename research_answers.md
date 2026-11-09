# Research answers

## 1. Preserving state, authentication and sessions

HTTP is stateless: each request is processed independently, so an application needs a way to recognise related requests. A common solution is a session. After a visitor interacts with the application, the server can create a session record and send a session identifier in a browser cookie. The browser returns that cookie on later requests, allowing the server to retrieve the associated state. Django's default session backend stores session data in the database; the cookie normally carries the identifier rather than all the session data. SessionMiddleware makes this state available through request.session. During authentication, Django verifies credentials and records authentication information in the session, allowing AuthenticationMiddleware to populate request.user on subsequent requests. The password does not need to be sent with every page request. Django rotates session keys at login to reduce session-fixation risks, while logout clears the current session. Session expiry limits how long state remains usable. Production applications should use HTTPS, secure cookie settings and CSRF protection for state-changing forms. Finally, identifying a logged-in user does not automatically authorise access to every record: each protected view must also enforce the relevant permissions and ownership rules.

Sources:

- [Django: How to use sessions](https://docs.djangoproject.com/en/5.2/topics/http/sessions/)
- [Django: Using the authentication system](https://docs.djangoproject.com/en/5.2/topics/auth/default/)
- [MDN: HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)

## 2. Django migrations with MariaDB

To migrate a Django application to MariaDB, first choose a server version supported by the project's Django release and install the recommended Python driver, mysqlclient, in the virtual environment. Django accesses MariaDB through django.db.backends.mysql. Create an empty database using the utf8mb4 character set and a dedicated account with the database privileges needed to apply migrations. Configure DATABASES with the database name, user, password, host and port, keeping credentials outside version control. Use InnoDB tables and enable a strict SQL mode to reduce silent data truncation. After changing application models locally, run python manage.py makemigrations and inspect the resulting migration files. Commit those files with the code; do not independently regenerate them on each server. Before deployment, back up existing server data and test the same migrations against a staging database. On the target server, install the pinned dependencies, provide the database configuration, inspect python manage.py showmigrations and python manage.py migrate --plan, then run python manage.py migrate. Check the resulting tables and exercise the application afterwards. Migrations create or change the schema; moving existing records from SQLite is a separate, planned data-transfer step. MySQL-family schema changes may not be transactionally reversible, so tested backups and recovery procedures remain important.

Sources:

- [Django: MariaDB and MySQL database notes](https://docs.djangoproject.com/en/5.2/ref/databases/)
- [Django: Migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/)
- [Django: migrate command](https://docs.djangoproject.com/en/5.2/ref/django-admin/#migrate)

These findings describe deployment procedures. The submitted app uses SQLite;
no MariaDB server was configured or migrated as part of this local project.
