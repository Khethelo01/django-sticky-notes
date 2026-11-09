# Sticky Notes - Django Application Part 1

This submission includes both practical parts: a working Django project and
the two research answers. It follows the main assignment and the additional
Django Project Setup guide. The project is named `sticky_notes`; the app is
named `notes`.

## Start here

Extract the ZIP to a writable folder. Use Python 3.10 or newer (verified with
Python 3.14). Open a terminal in this folder, next to `requirements.txt`.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cd sticky_notes
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in a browser. Keep the terminal running while
using the application. Press **Ctrl+C** to stop the development server.
Use **New note** to add a title and content, **Open note** to read it,
**Edit note** to update it, and **Delete note** to reach a confirmation page.
**Keep note** cancels deletion. Notes persist after closing the browser or
restarting the server.

If PowerShell blocks activation, call the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe sticky_notes\manage.py migrate
.\.venv\Scripts\python.exe sticky_notes\manage.py collectstatic --noinput
.\.venv\Scripts\python.exe sticky_notes\manage.py runserver
```

On macOS/Linux, activate with `source .venv/bin/activate` instead.

## What is included

| Requirement | Implementation |
| --- | --- |
| Use case, sequence and class diagrams | `design/sticky_notes_design.pdf`, one diagram per page |
| Project named sticky_notes | `sticky_notes/manage.py` and its inner `sticky_notes` package |
| Installed application | `notes.apps.NotesConfig` in `INSTALLED_APPS` |
| Note model | Title, content, primary key, creation time and update time |
| Database migrations | `notes/migrations/0001_initial.py`; migrations were applied locally |
| CRUD views | `notes/views.py` handles list, detail, create, update and delete |
| Forms | `notes/forms.py` supplies a reusable, validated `NoteForm` |
| URL routing | `notes/urls.py` is included by the main project URL configuration |
| Base template | `notes/templates/base.html` supplies shared layout and navigation |
| Page templates | Board, detail, create/edit form and delete confirmation |
| CSS | `notes/static/notes/styles.css`, loaded with the static template tag |
| Static collection | `STATIC_ROOT` points to `staticfiles`; collectstatic was verified |
| PEP 8 and testing | Flake8 configuration and 19 passing Django tests |
| Research answers | `research_answers.md`, with two paragraphs and linked sources |
| Reproducible environment | Pinned `requirements.txt`, generated from the isolated environment |

## Project structure and MVT

```text
Sticky Notes Submission/
  README.md
  requirements.txt
  research_answers.md
  verification.txt
  design/
    sticky_notes_design.pdf
  sticky_notes/
    manage.py
    sticky_notes/
      settings.py, urls.py, asgi.py, wsgi.py
    notes/
      models.py, forms.py, views.py, urls.py, admin.py, apps.py, tests.py
      migrations/0001_initial.py
      templates/base.html
      templates/notes/
        note_list.html, note_detail.html, note_form.html
        note_confirm_delete.html
      static/notes/styles.css
```

**Model:** `Note` defines persistent data and is mapped to SQLite by Django's
ORM. Notes appear in most-recently-updated order. Title is limited to 200
characters; title and content cannot be blank. Creation time remains stable
when editing, while update time changes automatically.

**View:** Python view functions retrieve data, validate submitted forms,
save or delete records and choose a template or redirect. A successful POST
redirects to avoid repeating a mutation on page refresh. A missing note
returns HTTP 404. GET requests never delete records.

**Template:** Pages extend `base.html`, use named URL routes, escape user
content and load the app's CSS through Django's static-file system. Forms
contain CSRF tokens, labelled fields and visible validation feedback.

The app is a local, shared notes board, matching the scope of Part 1. User
accounts and per-user note ownership are not implemented. The research
document discusses authentication/session management separately. The default
settings and fallback secret key are for local coursework. Any public
deployment needs its own secret, production settings and access controls.

## Checks

With the environment activated, from the inner project directory containing
`manage.py`:

```text
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test -v 2
python manage.py collectstatic --noinput
python -m flake8 .
```

The tests check CRUD, persistence through ORM reads, invalid forms, timestamp
behaviour, HTML escaping, CSRF enforcement, HTTP method handling, missing
records, template inheritance and static-file discovery. The app was also
tested in a real browser on desktop and mobile, including create, edit,
reload, cancel deletion and confirmed deletion. See `verification.txt`.

An admin account is optional. Run `python manage.py createsuperuser` and
choose your own credentials to use `/admin/`. None are included in the ZIP.

## Migrations and static files

The supplied migration file must stay in the submission. Run `migrate` on a
fresh machine to create the SQLite database; do not delete migrations or
generate a replacement merely to start the app. For future model changes,
run `makemigrations` and then `migrate`.

The default app static finder discovers the namespaced CSS automatically.
`collectstatic` copies source assets into `staticfiles`. With `DEBUG=True`,
the development server serves app static assets without requiring collection;
the collection configuration is nevertheless provided and was verified.

The ZIP intentionally excludes virtual environments, Python caches, the local
SQLite database and collected static copies. These are generated locally.
All source CSS, templates, Python modules and migrations are included.

## Submission

Review the app, diagrams and research answers. Upload the ZIP if accepted,
or upload the extracted project files together inside your task folder.
Then select **Request review**. No dashboard submission was made for you.
