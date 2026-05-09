# AutoShop Pro — Step-by-step

This repository contains the AutoShop Pro web app built with Django. Below is my best attempt at clear instructions for someone who isn't technically inclined.

Prerequisites:
- Windows 10+
- Python3.11+
- Node.js
- Extract the project anywhere
- Rename the project 'a_shop' (no longer an issue)
 
**Quick Start (Windows Only):** 

1. Move to the project directory:
<img width="1918" height="137" alt="step1" src="https://github.com/user-attachments/assets/050e9319-aa56-4248-97cd-14eb2feb8b4f" />


Run in powershell

2. Create a virtual environment:
<img width="1918" height="25" alt="step2" src="https://github.com/user-attachments/assets/f1f55d78-f3c7-4370-b631-aa6e163e29d8" />


`python -m venv .venv`
This creates a local virtual environment

3. Activate the virtual environment:
<img width="1918" height="33" alt="step3" src="https://github.com/user-attachments/assets/dde0ffb7-53a0-4fa5-9dd4-5d9acef9ea4e" />


`.\.venv\Scripts\Activate.ps1`

4. Install external libraries:
<img width="1917" height="458" alt="step4" src="https://github.com/user-attachments/assets/4c435191-0088-4a52-8883-7d9229472233" />


`python -m pip install -r requirements.txt` or
`python -m pip install django requests`
(requests not shown in picture)

5. Close powershell, move to file explorer

- Run `.\install.ps1` to install dependencies in powershell
<img width="1038" height="887" alt="ps1_install" src="https://github.com/user-attachments/assets/1e56c76c-4c50-4eb7-8a55-cca0c04822b5" />
For the sole powershell (install.ps1) script, left-click, then right click. When the menu appears, click on 'Run with powershell'


- Run `.\initialize.bat` to set up the database in cmd (you can double click the .bat files like normal)
<img width="1920" height="1080" alt="initialize_script" src="https://github.com/user-attachments/assets/6142122f-8abe-4ef3-a7fc-43dcc1a6be2f" />


This batchfile asks you to create a username, email, and password.
DO NOT LOSE THIS PASSWORD. I CAN NOT HELP YOU RECOVER IT!
It also asks about demo data, which currently has to be deleted manually.

- Run `.\run.bat` to start the app in cmd
<img width="1920" height="1080" alt="server_running" src="https://github.com/user-attachments/assets/9a8c2d3f-1392-451a-8663-0da99794723d" />


The server should now start, available at 127.0.0.1:8000, and can be stopped using Ctrl+C in the cmd.

**Important:**
When this guide references files, they are paths inside the project. For example, the settings file is `autoshop/settings.py` and templates live under `templates/`.
- If you see an execution policy error, run this first in powershell:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- The 'install.ps1' script attempts to auto-install Python and Node.js. However, this guide relies on you installing them beforehand.
- **Python3.11+**: Download from https://www.python.org/downloads/ **(check "Add Python to PATH" during installation)**
- **Node.js**: Download running `winget install OpenJS.NodeJS` in powershell or https://nodejs.org/ (npm comes with it)

How to use/key features:

- Workflow / Kanban board: Click "Workflow" in the left sidebar. Drag a job card from one column to another to update its status. The board now moves cards instantly (optimistic update) and keeps the server in sync.
- Add a job: Click "+ New Job" on the dashboard or workflow pages and fill out the form.
- Job details: Open a job and click "View" to see parts, costs, and status. If you're a manager (staff user), you will see a "Delete" button.
<img width="1920" height="1080" alt="job_board" src="https://github.com/user-attachments/assets/ed9f2278-f842-4667-97bb-4cfce7585062" />

- Customers & Vehicles: Use the "Customers" and "Vehicles" pages to add or edit records. Using the vin field while adding a new vehicle, you can leverage the built in vin decoder to autofill some fields!
<img width="1920" height="1080" alt="vin_decode" src="https://github.com/user-attachments/assets/850abb60-7fc6-4dcd-8694-0a5fe368187e" />

- Inventory: Use the "Inventory" page to view and manage parts.
<img width="1920" height="1080" alt="inventory" src="https://github.com/user-attachments/assets/be9f5993-6e24-4ac5-a99d-edbc0726e615" />

- Reports: Not fully implimented. Planning on a financial focus and/or exporting documents/reports for jobs.

- Dashboard: Congregates all job info with an interactive calender, recent job list, and overview of upcoming jobs.
<img width="1920" height="1080" alt="dashboard" src="https://github.com/user-attachments/assets/9abe004b-ca46-48ed-a38e-927f92c0fd40" />


v1.2 Changelog:
- fixed kanban board mostly
- integrated vin decoder and vin caching
- added front end guardrails for impromper job scheduling and kanban conflicts

Planned improvements:
- Image/attachment upload in notes. im thinking voice notes could be useful as well as pictures.
- Open access network wide; not just loopback.
- Use PostgreSQL for production: change `DATABASES` in `autoshop/settings.py` and install PostgreSQL server.
- Add activity logs to track who changed job status when.
- Implement richer reports (CSV export) and scheduled backups. (reports tab)

Troubleshooting tips:
- If pages look unstyled, confirm you ran `npm run build:css` and that `static/css/style.css` exists.
- If you see database errors, re-run `python manage.py migrate` and ensure the virtual environment is activated.
- If you forget your superuser password, run `python manage.py createsuperuser --username manager --email manager@example.com` to recreate or use the Django admin to reset passwords.


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

How to stop the local server:

Press Ctrl+C in the PowerShell window where `runserver` is running.

