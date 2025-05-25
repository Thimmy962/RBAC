# 📘 API References

This document provides a reference for all available API endpoints in the **RBAC for Library Management System** project. All endpoints are RESTful and follow standard naming and behavior conventions.

---

# 📘 API References

> **Note:** All endpoints listed below (except for the authentication routes) are prefixed with `/api/` via the main project's `urls.py` file where the app-level URLs are included as:
>
> ```python
> path("api/", include("api.urls"))
> path("graph/", GraphQLView.as_view(graphiql = True))
> ```
> 
> This means all except get request routes (e.g., users, books, authors) are accessed under the `/api/` prefix.
> All get request are accessed with no just `/graph?query = query {....}` and the query 

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

### 🔸 Create Staff

**POST** `/api/users/`  
**Description:**   
- `POST`: Create a new staff user.


### 🔸 Update or Delete a Staff

**PUT/PATCH/DELETE** `/api/user/<int:pk>`  
**Description:**  
Manage a single staff user by their primary key (`pk`).

---

## 👥 Group/Role Management


**POST** `/api/groups/`  
**Description:**    
- `POST`: Create a new role/group.

### 🔸 Update or Delete a Role

**PUT/PATCH/DELETE** `/api/group/<int:pk>`  
**Description:**  
Manage a specific role/group by its primary key (`pk`).  


---

## 🎭 Genre Management

### 🔸 Create Genre

**POST** `/api/genres/`  
**Description:**  
- `POST`: Create a new genre.

### 🔸 Update or Delete a Genre

**PUT/PATCH/DELETE** `/api/genre/<int:pk>`  
**Description:**  
Manage a single genre by its primary key.

---

## ✍️ Author Management

### 🔸 Create Author

**POST** `/api/authors/`  
**Description:**  
- `POST`: Create a new author.

### 🔸 Update or Delete an Author

**PUT/PATCH/DELETE** `/api/author/<int:pk>`  
**Description:**  
Manage a single author by primary key.

---

## 📚 Book Management

### 🔸 Create Book

**POST** `/api/books/`  
**Description:**
- `POST`: Create a new book.

### 🔸 Update or Delete a Book

**PUT/PATCH/DELETE** `/api/book/<str:pk>`  
**Description:**  
Manage a single book by primary key (can be a string, e.g., accession number or UUID).

---

## 🔁 Status Codes

All API responses follow standard HTTP status codes:
- This applies to the Post, update, and Delete Requets 

- `200 OK` – Success  
- `201 Created` – Resource created  
- `204 No Content` – Successfully deleted  
- `400 Bad Request` – Invalid input  
- `401 Unauthorized` – Authentication required  
- `403 Forbidden` – Permission denied  
- `404 Not Found` – Resource not found

- Get Requests uses graphql which send:
- `200 OK` – Success; alone

Errors in `graph` api is detected by checking for the ##errors## field in the response
---

## 📝 Notes

- All endpoints require authentication via JWT.  
- Ensure to include `Authorization: Bearer <access_token>` in the request header.

---

For usage examples and payload samples, please refer to the project documentation or test endpoints with Postman.
