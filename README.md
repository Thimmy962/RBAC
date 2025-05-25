# This Branch was created so that every get request will be offloaded to graphQL
# This way, frontend can dyanmically retrieve data without waiting for backend to add another api

# Role-Based Access Control (RBAC) for Library Management System

A Django-based backend system that manages **staff access to library resources** using **role-based access control**. It controls what staff can access and the actions they are permitted to carry out within the system.

---

## 📌 Summary

This project implements a role-based access control system for managing:

- Staff members  
- Roles and role-specific permissions  
- Access to resources based on group permissions

---

## ✅ Key Features

- Staff account management  
- Role and group management  
- Fine-grained permission control per role/group  
- Secure authentication with JSON Web Tokens (JWT)

---

## 🛠️ Technology Stack

- Python 3.10+  
- Django  
- Django REST Framework  
- Simple JWT (JSON Web Token authentication)

---

## 🔧 Prerequisites

- Python 3.10+  
- Pip

---

## 🚀 Setup Instructions

### 1. Create a Virtual Environment

```bash
pip install virtualenv
python3 -m venv env
source env/bin/activate  # Use `env\Scripts\activate` on Windows
```

### 2. Clone the Repository

```bash
git clone https://github.com/thimmy962/RBAC
cd RBAC
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Open `RBAC/settings.py` and adjust the following:

#### For Development:

```python
SECRET_KEY = "your_50_character_random_secret_key"
DEBUG = True
```

#### For Production:

```python
SECRET_KEY = "your_50_character_random_secret_key"
DEBUG = False
ALLOWED_HOSTS = ['your_production_domain_or_ip']
```

Update database settings as needed.

---

## ⚙️ Run the Project

### Development Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the admin account.

### Production (Example with Gunicorn)

```bash
gunicorn RBAC.wsgi
```

---

## 📄 API Usage

Refer to the `api_references.md` file for complete documentation of the available endpoints.

---

## 📁 Project Structure

```
RBAC/
├── .github/
│   └── workflows/
│       └── work.yml
├── api/
│   ├── tests/
│   ├── utils/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── urls.py
│   └── views.py
├── RBAC/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📬 Contribution & Feedback

Feel free to fork this repository, submit issues, or open pull requests for improvements. Feedback is always welcome!

## 📬 Contribution & Feedback

## 👨‍⚖️ Middleware

- A custom middleware (SimpleJWTGraphQLMiddleware) was written to solve the incompatibility in authenticating user issue graphene has with JWT
- Another (MaintenanceMiddleware) was written for maintenance purposes

check API.utils.middleware for their definiton

When undergoing maintenance:
- set settings.MAINTENANCE_MODE to True
