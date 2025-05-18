# 📘 API References

This document provides a reference for all available API endpoints in the **RBAC for Library Management System** project. All endpoints are RESTful and follow standard naming and behavior conventions.

---

# 📘 API References

> **Note:** All endpoints listed below (except for the authentication routes) are prefixed with `/api/` via the main project's `urls.py` file where the app-level URLs are included as:
>
> ```python
> path("api/", include("api.urls"))
> ```
> 
> This means all app routes (e.g., users, books, authors) are accessed under the `/api/` prefix.

---


## 🔐 Authentication

### 🔸 Obtain Token

**POST** `/api/token/`  
**Description:** Obtain a pair of access and refresh tokens.

### 🔸 Refresh Token

**POST** `/api/token/refresh/`  
**Description:** Refresh the access token using a valid refresh token.

---

## 👤 Staff Management

### 🔸 List or Create Staff

**GET/POST** `/api/users/`  
**Description:**  
- `GET`: Retrieve a list of all staff users.  
- `POST`: Create a new staff user.

### 🔸 Retrieve, Update or Delete a Staff

**GET/PUT/PATCH/DELETE** `/api/user/<int:pk>`  
**Description:**  
Manage a single staff user by their primary key (`pk`).

---

## 👥 Group/Role Management

### 🔸 List or Create Role

**GET/POST** `/api/groups/`  
**Description:**  
- `GET`: Retrieve a list of all roles/groups.  
- `POST`: Create a new role/group.

### 🔸 Retrieve, Update or Delete a Role

**GET/PUT/PATCH/DELETE** `/api/group/<int:pk>`  
**Description:**  
Manage a specific role/group by its primary key (`pk`).  


---

## 🎭 Genre Management

### 🔸 List or Create Genre

**GET/POST** `/api/genres/`  
**Description:**  
- `GET`: List all book genres.  
- `POST`: Create a new genre.

### 🔸 Retrieve, Update or Delete a Genre

**GET/PUT/PATCH/DELETE** `/api/genre/<int:pk>`  
**Description:**  
Manage a single genre by its primary key.

---

## ✍️ Author Management

### 🔸 List or Create Author

**GET/POST** `/api/authors/`  
**Description:**  
- `GET`: Retrieve all authors.  
- `POST`: Create a new author.

### 🔸 Retrieve, Update or Delete an Author

**GET/PUT/PATCH/DELETE** `/api/author/<int:pk>`  
**Description:**  
Manage a single author by primary key.

---

## 📚 Book Management

### 🔸 List or Create Book

**GET/POST** `/api/books/`  
**Description:**  
- `GET`: Retrieve all books.  
- `POST`: Create a new book.

### 🔸 Retrieve, Update or Delete a Book

**GET/PUT/PATCH/DELETE** `/api/book/<str:pk>`  
**Description:**  
Manage a single book by primary key (can be a string, e.g., accession number or UUID).

---

## 🔁 Status Codes

All API responses follow standard HTTP status codes:

- `200 OK` – Success  
- `201 Created` – Resource created  
- `204 No Content` – Successfully deleted  
- `400 Bad Request` – Invalid input  
- `401 Unauthorized` – Authentication required  
- `403 Forbidden` – Permission denied  
- `404 Not Found` – Resource not found

---

## 📝 Notes

- All `POST`, `PUT`, and `PATCH` endpoints require authentication via JWT.  
- Ensure to include `Authorization: Bearer <access_token>` in the request header.

---

For usage examples and payload samples, please refer to the project documentation or test endpoints with Postman.
