# AutoShop Pro

This repository contains the AutoShop Pro web app built with Django. Below is my best attempt at clear instructions for someone who isn't technically inclined.

Prerequisites:
- Windows 10+
- Python3.11+
- Node.js
- Extract the project anywhere
- Rename the project 'a_shop' (no longer an issue)
 
**Quick start using powershell:** 

1. Move to the project directory:
<img width="1918" height="137" alt="step1" src="https://github.com/user-attachments/assets/050e9319-aa56-4248-97cd-14eb2feb8b4f" />


```bash
cd DriveLetter:\...\a_shoppro-main
```
or
```bash
cd DriveLetter:\...\a_shop
```
if you changed the filename.

2. Create a virtual environment:
<img width="1918" height="25" alt="step2" src="https://github.com/user-attachments/assets/f1f55d78-f3c7-4370-b631-aa6e163e29d8" />


```bash
python -m venv .venv
```
This creates a local virtual environment

3. Activate the virtual environment:
<img width="1918" height="33" alt="step3" src="https://github.com/user-attachments/assets/dde0ffb7-53a0-4fa5-9dd4-5d9acef9ea4e" />


```bash
.\.venv\Scripts\Activate.ps1
```

4. Install external libraries:
<img width="1917" height="458" alt="step4" src="https://github.com/user-attachments/assets/4c435191-0088-4a52-8883-7d9229472233" />


```bash
python -m pip install -r requirements.txt
``` 
or
```bash
python -m pip install django requests pillow
```
(requests & pillow not shown in picture)

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
<img width="2560" height="1392" alt="run1" src="https://github.com/user-attachments/assets/c9e641cd-2238-4e02-b104-7553c4247f8e" />

This will ask if you want to start the application on device-only or network wide

<img width="2566" height="1392" alt="run2" src="https://github.com/user-attachments/assets/985b71be-5e8c-4d5d-a3f2-51aecdb20d3b" />

If option 2 is chosen, the access address will be displayed in the terminal while the app is running.
To access the app on another machine, simply type the provided IP into any browser on any device on the same network.
Press Ctrl+C in the PowerShell window where `run.bat` is running to stop the application safely.

**Important:**
When this guide references files, they are paths inside the project. For example, the settings file is `autoshop/settings.py` and templates live under `templates/`.
- If you see an execution policy error, run this first in powershell:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- You may have to disable 'Smart App Control' in Windows Defender
- The 'install.ps1' script attempts to auto-install Python and Node.js. However, this guide relies on you installing them beforehand.
- **Python3.11+**: Download from https://www.python.org/downloads/ **(check "Add Python to PATH" during installation)**
- **Node.js**: Download running `winget install OpenJS.NodeJS` in powershell or https://nodejs.org/ (npm comes with it)

How to use/key features:

- Workflow / Kanban board: Click "Workflow" in the left sidebar. Drag a job card from one column to another to update its status. The board now moves cards instantly (optimistic update) and keeps the server in sync.
- Add a job: Click "+ New Job" on the dashboard or workflow pages and fill out the form.
- Job details: Open a job and click "View" to see parts, costs, and status. If you're a manager (staff user), you will see a "Delete" button.
<img width="1920" height="1080" alt="job_board" src="https://github.com/user-attachments/assets/ed9f2278-f842-4667-97bb-4cfce7585062" />

- Customers & Vehicles: Use the "Customers" and "Vehicles" pages to add or edit records. Using the vin field while adding a new vehicle, you can leverage the built in vin decoder to autofill some fields. Now fully supports by-job attachment uploads (voice recording, picture, or text file).
<img width="1920" height="1080" alt="jobform1" src="https://github.com/user-attachments/assets/67cf6afc-3fe1-475e-9919-da0d79da8cdf" />

In the job view/editing tab, you can see an attachment thumbnail if applicable, add a note, download the file, and delete them.

- Inventory: Use the "Inventory" page to view and manage parts.
<img width="1920" height="1080" alt="inventory" src="https://github.com/user-attachments/assets/be9f5993-6e24-4ac5-a99d-edbc0726e615" />

- Reports: Not fully implimented. Planning on a financial focus and/or exporting documents/reports for jobs.

- Dashboard: Congregates all job info with an interactive calender, recent job list, and overview of upcoming jobs.
<img width="1920" height="1080" alt="dashboard" src="https://github.com/user-attachments/assets/9abe004b-ca46-48ed-a38e-927f92c0fd40" />

- Wireless/Mobile network access:
<img width="645" height="1398" alt="IMG_3600" src="https://github.com/user-attachments/assets/a8e9f43b-55ce-4ed5-9edc-8069338ff5fe" />

With the addition of network configuration in `run.bat`, you can now access the application from across your network including on mobile. Though, the kanban board is not fully functional on mobile.

v1.4.1 Changelog:
- Attachment uploads & notes
- Network access
- Polished login page
- Expanded demo data
- touch-up kanban board scheduling restrictions

Known Issues:
- Demo data initialization says '0 jobs added', when it adds ~15 jobs
- Some demo data will be overwritten on edit due to auto vin decoding
- Kanban is not interactive on mobile

Planned improvements:
- Polish mobile UI
- Autofill for common jobs (can vary between shops)
- Low part availability alert(s)
- Use PostgreSQL for production: change `DATABASES` in `autoshop/settings.py` and install PostgreSQL server.
- Add activity logs to track who changed job status when.
- Implement richer reports (CSV export) and scheduled backups. (reports tab)

## Manual Way 

1) Create and activate a Python virtual environment

Open PowerShell in the project folder (the folder that contains `manage.py`). Then run these commands, one line at a time:

```bash
cd a_shop
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- The first command creates an isolated Python environment in a hidden folder called `.venv`.
- The second command switches your terminal to use the environment. You should see `(.venv)` appear at the start of the prompt.

With the virtual environment activated, install dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs Django. For local development use SQLite is used.

3) Initialize the database (migrations)

Run these commands to create the database tables and a demo manager user:

Follow the prompts to enter a username (for example `manager`), email (optional), and password.

```bash
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

```bash
npm install
npm run build:css
```

That creates `static/css/style.css` locally.

If you want CSS to rebuild automatically while you edit templates, run this in a second terminal:

```bash
npm run watch:css
```

5) Run the development server

Start the app locally:

```bash
python manage.py runserver
```

Open a web browser and go to `http://127.0.0.1:8000/`. You should see the AutoShop Pro UI.

6) Log in

- Click "Sign in" and use the superuser credentials you created with `createsuperuser` (or `manager` if you used the seed command).
- Admin interface is at `http://127.0.0.1:8000/admin/` if you need to manage data directly.

How to stop the local server:

Press Ctrl+C in the PowerShell window where `runserver` is running.

Troubleshooting tips:
- If pages look unstyled, confirm you ran `npm run build:css` and that `static/css/style.css` exists.
- If you see database errors, re-run `python manage.py migrate` and ensure the virtual environment is activated.
- If you forget your superuser password, run `python manage.py createsuperuser --username manager --email manager@example.com` to recreate or use the Django admin to reset passwords.

### Migrations

Running `python manage.py makemigrations` produced migrations to add the `is_demo_data` fields; run migrations locally to apply them:

```bash
python manage.py makemigrations
python manage.py migrate
```

### How to use the new demo tools

Seed demo data (idempotent):

```bash
python manage.py seed_demo_data
# or seed after cleaning up existing demo data
python manage.py seed_demo_data --cleanup
```

Delete all demo data (interactive):

```bash
python manage.py delete_demo_data
# non-interactive (CI/scripts):
python manage.py delete_demo_data --no-confirm
```

### Notes

- After seeding, scheduled demo jobs will appear in the Kanban column "Scheduled (Next 36 Hours)".
- The server-side scheduling validation now permits a 30-minute grace window for moving jobs back to `WAITING`. If you prefer this value configurable, I can add a setting (e.g. `JOB_SCHEDULE_GRACE_MINUTES`) and wire it into the validation.

If you'd like, I can also update the admin or list views to display an `is_demo_data` badge for easier identification of demo records.
