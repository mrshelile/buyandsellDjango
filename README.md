# Buy and Sell Django API

A Django-based backend project for a buy-and-sell marketplace application. The project provides a REST API for managing users, products, banners, featured ads, car listings, and related content. It uses Django REST Framework and SQLite for local development.

## Project Overview

This application allows you to:

- Register and authenticate users
- Create and manage product listings
- Upload multiple product images
- Manage banners and featured advertisements
- Handle user account validation and password reset flows
- Expose REST API endpoints for frontend/mobile consumption

## Tech Stack

- Python 3.x
- Django 4.1.3
- Django REST Framework
- Django Filters
- SQLite
- Pillow for image uploads

## Project Structure

- `buyandsellDjango/` – main Django project settings and routing
- `content/` – app containing models, views, serializers, and API routes
- `uploads/` – media files uploaded by users
- `static/` – static files for the project
- `db.sqlite3` – local SQLite database file

## Prerequisites

Before running the project, make sure you have:

- Python installed on your machine
- `pip` available
- Access to a terminal or PowerShell

## Installation on Windows

1. Open PowerShell and navigate to the project folder:

   ```powershell
   cd "f:\Documents\Projects Worked On\BuyAndSell\buyandsellDjango"
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .env
   .\.env\Scripts\Activate.ps1
   ```

3. Install the required packages:

   ```powershell
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```powershell
   python manage.py migrate
   ```

5. Create a superuser account for the Django admin panel:

   ```powershell
   python manage.py createsuperuser
   ```

## Running the Project

Start the development server:

```powershell
python manage.py runserver 0.0.0.0:8000
```

The app will be available at:

- Localhost: http://127.0.0.1:8000/
- Local network access: http://<your-local-ip>:8000/

For example, if your laptop IP is `192.168.1.59`, you can access it using:

```text
http://192.168.1.59:8000/
```

## API Routes

The API is exposed under the `buyandsellDjango-apis/` base route. Some of the main endpoints include:

- `/buyandsellDjango-apis/` – base API routes
- `/buyandsellDjango-apis/auth/` – authentication-related endpoints
- `/buyandsellDjango-apis/sendEmail/` – email sending endpoint
- `/buyandsellDjango-apis/reset-password` – password reset route
- `/buyandsellDjango-apis/update-password` – password update route
- `/buyandsellDjango-apis/validate-account` – account validation route

## Admin Panel

You can access the Django admin panel at:

```text
http://127.0.0.1:8000/admin/
```

Log in with the superuser credentials you created earlier.

## Media Files

Uploaded images and files are stored in the `uploads/` directory. These are served through the project’s media URL configuration.

## Common Development Commands

Run system checks:

```powershell
python manage.py check
```

Run tests:

```powershell
python manage.py test
```

Create new migrations after changing models:

```powershell
python manage.py makemigrations
```

## Troubleshooting

If you encounter issues:

- Make sure your virtual environment is activated
- Confirm that all packages were installed successfully
- Check that the correct Python interpreter is being used
- If port `8000` is already in use, try another port such as:

  ```powershell
  python manage.py runserver 0.0.0.0:8080
  ```

## Notes

This project is intended for local development and testing. For production deployment, you should configure a production-ready web server, environment variables, and secure settings.
