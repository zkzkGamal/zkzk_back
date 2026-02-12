# Portfolio Backend

This is the backend API for a personal portfolio website, built with Django and Django REST Framework.

## Features

- **User Authentication:** Secure login and registration system.
- **Project Management:** Create, read, update, and delete project posts.
- **Rich Text Editing:** Integrated CKEditor for rich content in posts.
- **Real-time Notifications:** Uses Django Channels for real-time user notifications.
- **API Endpoints:** RESTful APIs for profile management, resume handling, and comments.
- **Search & Filtering:** Advanced filtering capabilities for project posts.

## Tech Stack

- **Python**
- **Django**
- **Django REST Framework (DRF)**
- **SQLite** (Default database)
- **Django Channels** (WebSockets)

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd zkzk_back
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The API should now be accessible at `http://127.0.0.1:8000/`.
