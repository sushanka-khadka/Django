# Django Meetups Project

This project is a Django-based web application for managing and registering for meetups. It provides features for listing meetups, viewing details, and user registration. The project is containerized with Docker and includes configuration for Nginx and static file management.

## Demo
https://github.com/user-attachments/assets/d3c46f08-bb4d-416a-952c-10a65524a419

## Features
- List all available meetups
- View detailed information about each meetup
- Register for meetups
- Admin interface for managing meetups
- Static and media file handling
- Docker and Nginx support for deployment

## Project Structure
- `DJANGO_SITE/` - Main Django project settings and configuration
- `meetups/` - Django app for meetup functionality (models, views, templates, static files)
- `staticfiles/` - Collected static files for production
- `uploads/` - Uploaded media files (e.g., images)
- `nginx/` - Nginx configuration for serving the app
- `meetup_venv/` - Python virtual environment (local development)
- `Dockerfile` and `compose.yaml` - Docker configuration files
- `requirements.txt` - Python dependencies

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd <project-directory>
```

### 2. Create and Activate Virtual Environment (Optional)
```bash
python -m venv meetup_venv
# Windows:
meetup_venv\Scripts\activate
# macOS/Linux:
source meetup_venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

### 6. Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### 7. Using Docker (Optional)
Build and run the app with Docker Compose:
```bash
docker compose up --build
```

## Deployment
- Nginx is configured to serve static files and proxy requests to the Django app.
- Update `nginx/default.conf` as needed for your deployment environment.

## License
This project is licensed under the MIT License.