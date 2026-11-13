# Buy and Sell Django – Production Deployment Guide

## 1. Overview

This document describes the deployment procedure for the Buy and Sell Django application hosted on **Zeecom cPanel**.

The application uses Git for source-code management and the `production` branch as the deployment branch.

### Deployment workflow

```text
Developer Machine
       |
       | 1. Commit changes
       | 2. Push to GitHub
       v
GitHub Repository
       |
       | production branch
       v
Zeecom Hosting (cPanel)
       |
       | 3. Pull latest production changes
       | 4. Install dependencies
       | 5. Apply migrations
       | 6. Collect static files
       | 7. Restart application
       v
Live Buy and Sell Application
```

## 2. Git Branch Structure

The project uses the following branches:

| Branch | Purpose |
|---|---|
| `localWindows` | Local Windows development |
| `master` | Main development and integration branch |
| `production` | Live deployment branch |

All changes intended for the live application must eventually be merged into `production`.

**Important:** Do not push unfinished development changes directly to `production`.

## 3. Step 1 – Prepare changes locally

Open the project directory:

```bash
cd /path/to/buyandsellDjango
```

Check the current branch:

```bash
git branch
git status
```

Ensure that the application is working correctly before deploying.

Run Django checks:

```bash
python manage.py check
```

Review pending migrations:

```bash
python manage.py makemigrations --check
python manage.py migrate --plan
```

If new migrations are required, generate and commit them:

```bash
python manage.py makemigrations
```

Review the generated migration files before committing.

## 4. Step 2 – Push changes to GitHub

Push the relevant development branch:

```bash
git add .
git commit -m "Describe application updates"
git push origin master
```

If development was done on another branch, push that branch instead.

### Merge changes into production

Switch to the production branch:

```bash
git checkout production
git fetch origin
```

Update the local production branch:

```bash
git pull origin production
```

Merge the tested changes from master:

```bash
git merge master
```

If conflicts occur, resolve them carefully and test the application.

Once the merge is successful:

```bash
git push origin production
```

Verify:

```bash
git status
git log -1 --oneline
```

The latest production commit should contain the changes intended for deployment.

## 5. Step 3 – Access Zeecom cPanel

1. Log in to your Zeecom hosting account.
2. Open cPanel.
3. Navigate to **Git Version Control** or the Git repository management section.
4. Locate the Buy and Sell Django repository.
5. Open the repository deployment interface or cPanel Terminal.

Confirm that the repository is configured to use the `production` branch.

## 6. Step 4 – Pull the latest production changes

Navigate to the application directory on the server.

Example:

```bash
cd /home/USERNAME/buyandsellDjango
```

Check the current branch:

```bash
git branch
git status
```

Fetch the latest repository changes:

```bash
git fetch origin
```

Pull the production branch:

```bash
git pull origin production
```

If the repository is configured to track `origin/production`, this can also be used:

```bash
git pull
```

### If Git reports divergent branches

Do not immediately force-merge or overwrite the live server.

First inspect the differences:

```bash
git status
git log --oneline --graph --decorate -10
git diff HEAD origin/production
```

Check whether there are important server-side changes.

If the server contains no changes that need to be preserved, and the GitHub `production` branch is confirmed as the authoritative deployment source, synchronize carefully:

```bash
git fetch origin
git reset --hard origin/production
```

**WARNING:** `git reset --hard` discards uncommitted changes and local commits on the server. Back up any important changes first.

Never use this command without confirming that the remote production branch contains the correct application version.

## 7. Step 5 – Activate the Python virtual environment

Use the Python environment configured in cPanel.

Example:

```bash
source /home/USERNAME/virtualenv/buyandsellDjango/3.11/bin/activate
```

The actual path depends on the Python version and application configuration in cPanel.

Confirm Python and pip:

```bash
python --version
pip --version
```

## 8. Step 6 – Install or update dependencies

Install the application requirements:

```bash
pip install -r requirements.txt
```

Ensure the required packages are installed, including:

- Django
- Django REST Framework
- django-filter
- django-cors-headers
- mysql-connector-python
- python-dotenv

Use the versions specified in `requirements.txt` wherever possible.

## 9. Step 7 – Verify production environment variables

Ensure that the production `.env` file exists in the project root.

The file should contain the required configuration:

```dotenv
DEBUG=False

SECRET_KEY=YOUR_PRODUCTION_SECRET_KEY

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=your_email@maraka.co.ls
EMAIL_HOST_PASSWORD=your_email_password
```

Use the actual database and email credentials configured in cPanel.

**Security requirements:**

- Never commit `.env` to GitHub.
- Never expose production credentials in source code.
- Keep `DEBUG=False` in production.
- Ensure the application user has the required database permissions.
- Do not replace the production `.env` with a development `.env`.

## 10. Step 8 – Database backup and migrations

Before applying database migrations, back up the live database.

For MySQL, an example backup command is:

```bash
mysqldump -u DB_USER -p DB_NAME > backup_before_deployment.sql
```

Replace `DB_USER` and `DB_NAME` with the actual database details.

Review pending migrations:

```bash
python manage.py showmigrations
python manage.py migrate --plan
```

Apply migrations:

```bash
python manage.py migrate
```

Do not delete existing migrations or reset the production database as part of a normal deployment.

## 11. Step 9 – Collect static files

Run:

```bash
python manage.py collectstatic --noinput
```

This updates the static files collected by Django.

Confirm that the configured `STATIC_ROOT` directory exists and is writable by the application.

The web server must also be configured to serve the collected static files.

## 12. Step 10 – Restart the Django application

In cPanel:

1. Open **Setup Python App**.
2. Locate the Buy and Sell Django application.
3. Confirm the application directory and Python environment.
4. Click **Restart**.

If cPanel provides a restart file mechanism for the application, use the configured restart procedure.

Example:

```bash
touch tmp/restart.txt
```

Only use this command if the hosting configuration supports it.

## 13. Step 11 – Verify the live application

After restarting, verify:

- The website loads successfully.
- Django API endpoints respond correctly.
- User authentication works.
- Registration and login work.
- Database operations work.
- Email functionality works.
- Uploaded media files remain accessible.
- Static files load correctly.
- No unexpected server errors occur.

Run the production configuration check when needed:

```bash
python manage.py check --deploy
```

Check the cPanel application logs if the application fails to start.

## 14. Recommended deployment command sequence

For an ordinary deployment where the production branch is already synchronized and there are no server-side code changes:

```bash
# 1. Navigate to the project
cd /home/USERNAME/buyandsellDjango

# 2. Activate virtual environment
source /home/USERNAME/virtualenv/buyandsellDjango/3.11/bin/activate

# 3. Fetch production updates
git fetch origin

# 4. Pull production changes
git pull origin production

# 5. Install dependencies
pip install -r requirements.txt

# 6. Check Django configuration
python manage.py check

# 7. Review migrations
python manage.py migrate --plan

# 8. Apply migrations
python manage.py migrate

# 9. Collect static files
python manage.py collectstatic --noinput

# 10. Restart application
```

Restart the application through cPanel after completing the commands.

## 15. Deployment troubleshooting

| Problem | Recommended action |
|---|---|
| Git pull fails | Check branch tracking, local changes and remote divergence |
| Application fails to start | Inspect cPanel Python application logs |
| ModuleNotFoundError | Activate the correct virtual environment and install requirements |
| Database connection error | Verify `.env` database settings and MySQL permissions |
| Static files missing | Run `collectstatic` and verify the web server static configuration |
| 500 Internal Server Error | Inspect Django and cPanel error logs |
| Email delivery fails | Verify SMTP hostname, port, credentials and TLS configuration |
| Migration error | Review migration history and database backup before making changes |

## 16. Important production rules

1. `production` is the authoritative deployment branch.
2. Test changes before merging them into production.
3. Never overwrite the production `.env` file.
4. Always back up the live database before migrations.
5. Never commit database passwords, secret keys or other credentials.
6. Do not replace the live database with a local SQLite database.
7. Do not delete migration files to resolve migration problems.
8. Avoid force-pushing to the production branch.
9. Verify the live application after every deployment.
10. Keep a record of the deployed Git commit for rollback and troubleshooting.

---

**Deployment principle:** Development and integration take place locally. GitHub `production` contains the approved release. Zeecom cPanel retrieves that release and runs it using the production environment, database and application configuration.