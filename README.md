# AutoShop Pro — Step-by-step

This repository contains the AutoShop Pro web app built with Django. Below is my best attempt at clear instructions for someone who isn't technically inclined.

**Quick Start (Windows Only):** Double-click `run.bat` in the project folder. The app will start automatically.

Important: When this guide references files, they are paths inside the project. For example, the settings file is `autoshop/settings.py` and templates live under `templates/`.

Prerequisites (what you need on your computer):
- Python 3.10 or newer installed. You can check by opening a terminal and typing `python --version`.
- Basic terminal access, on Windows use PowerShell.

## Easy Way (Windows): Use the Launcher

The easiest way to run AutoShop Pro is to **double-click `run.bat`** in the project folder.

This will automatically:
1. Create a Python environment (if it doesn't exist)
2. Install all dependencies
3. Build the CSS files
4. Set up the database
5. Prompt you to create an admin account (enter username, email, password)
6. Start the server
7. Open the browser to `http://127.0.0.1:8000/`

That's it! The server keeps running. Press `Ctrl+C` in the terminal window to stop it.

**Alternative (PowerShell):** If the batch file doesn't work, open PowerShell in the project folder and run:
```
.\run.ps1
```

## Manual Way (if you prefer step-by-step control)

1) Create and activate a Python virtual environment

Open PowerShell in the project folder (the folder that contains `manage.py`). Then run these commands, one line at a time:

```
cd a_shop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- The first command creates an isolated Python environment in a hidden folder called `.venv`.
- The second command switches your terminal to use the environment. You should see `(.venv)` appear at the start of the prompt.

With the virtual environment activated, install dependencies listed in `requirements.txt`:

```
pip install -r requirements.txt
```

This installs Django. For local development we use SQLite (no extra setup).

3) Initialize the database (migrations)

Run these commands to create the database tables and a demo manager user:

Follow the prompts to enter a username (for example `manager`), email (optional), and password.
```
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
```

- `migrate` creates the database schema.
- `createsuperuser` creates an administrative account you can use to log in.
- `seed_demo_data` adds a small set of sample records (customers, a vehicle, a job, a part). If you already created a user named `manager`, the command will reuse it.

4) Build the local CSS once

This project is set up to work without any internet connection. It uses a locally built Tailwind CSS file instead of the Tailwind CDN.

If you have not done this yet, run:

```
npm install
npm run build:css
```

That creates `static/css/style.css` locally.

If you want CSS to rebuild automatically while you edit templates, run this in a second terminal:

```
npm run watch:css
```

5) Run the development server

Start the app locally:

```
python manage.py runserver
```

Open a web browser and go to `http://127.0.0.1:8000/`. You should see the AutoShop Pro UI.

6) Log in

- Click "Sign in" and use the superuser credentials you created with `createsuperuser` (or `manager` if you used the seed command).
- Admin interface is at `http://127.0.0.1:8000/admin/` if you need to manage data directly.

How to use key features:

- Workflow / Kanban board: Click "Workflow" in the left sidebar. Drag a job card from one column to another to update its status. The board now moves cards instantly (optimistic update) and keeps the server in sync.
- Add a job: Click "+ New Job" on the dashboard or workflow pages and fill out the form.
- Job details: Open a job and click "View" to see parts, costs, and status. If you're a manager (staff user), you will see a "Delete" button.
- Customers & Vehicles: Use the "Customers" and "Vehicles" pages to add or edit records. The VIN field is automatically uppercased.
- Inventory: Use the "Inventory" page to view and manage parts.
- Reports: Open "Reports" for quick daily/weekly summaries and revenue figures.

v1.1 Changelog:
- Added paginated job list with search and status filters (`jobs/urls.py`, `jobs/views.py`, `templates/jobs/job_list.html`).
- The Kanban board now uses an optimistic UI update (the card moves immediately without reloading the page). The JS file is at `static/js/kanban.js`.
- Added logging toggle in `autoshop/settings.py`.
- Switched the app to local compiled CSS so it can run offline.

Next steps and optional improvements:
- Use PostgreSQL for production: change `DATABASES` in `autoshop/settings.py` and install PostgreSQL server.
- Add role-based permissions so technicians have reduced access compared to managers.
- Add activity logs to track who changed job status when.
- Implement richer reports (CSV export) and scheduled backups.

Troubleshooting tips:
- If pages look unstyled, confirm you ran `npm run build:css` and that `static/css/style.css` exists.
- If you see database errors, re-run `python manage.py migrate` and ensure the virtual environment is activated.
- If you forget your superuser password, run `python manage.py createsuperuser --username manager --email manager@example.com` to recreate or use the Django admin to reset passwords.

Publishing checklist before you upload to GitHub:
- Do not commit `.venv/`, `venv/`, `node_modules/`, or `db.sqlite3`.
- Keep `.env` out of Git. Use `.env.example` as the safe template.
- Commit `package-lock.json` if you want repeatable CSS builds.
- Commit `static/css/style.css` so the app works offline after clone.

How to stop the local server:

Press Ctrl+C in the PowerShell window where `runserver` is running.

