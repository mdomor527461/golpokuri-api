# 📘 Golpokuri API Documentation

**Base URL:** `https://golpokuri-api.vercel.app`

---

## 🔐 Authentication

### 🔸 Register
- **URL:** `/register/`
- **Method:** `POST`
- **Body:**
```json
{
  "username": "johndoe",
  "password": "password123",
  "email": "johndoe@example.com",
  "user_type": "writer", // or "reader"
  "image": (optional image file)
}
```
- **Response:** User data

---

### 🔸 Login
- **URL:** `/login/`
- **Method:** `POST`
- **Body:**
```json
{
  "username": "johndoe",
  "password": "password123"
}
```
- **Response:**
```json
{
  "token": "your_token",
  "user_id": 1,
  "user_type": "writer"
}
```

---

### 🔸 Logout
- **URL:** `/logout/`
- **Method:** `POST`
- **Headers:** `Authorization: Token <your_token>`
- **Response:**
```json
{ "detail": "Logged out successfully" }
```

---

## 📚 Stories

### 🔸 Create Story
- **URL:** `story/create/`
- **Method:** `POST`
- **Headers:** `Authorization: Token <your_token>`
- **Body:**
```form-data
title: "My Story"
content: "Once upon a time..."
category: 1
image: (optional image file)
```
- **Response:** Created story data

---

### 🔸 List Stories
- **URL:** `story/stories/`
- **Method:** `GET`
- **Query Params (optional):**
  - `category=<category_id>`
  - `writer=<writer_id>`

---

### 🔸 Story Detail
- **URL:** `story/stories/<id>`
- **Method:** `GET`

---

### 🔸 Update Story
- **URL:** `story/stories/edit/<id>`
- **Method:** `PUT` or `PATCH`
- **Headers:** `Authorization: Token <your_token>`

---

### 🔸 Delete Story
- **URL:** `story/stories/delete/<id>`
- **Method:** `DELETE`
- **Headers:** `Authorization: Token <your_token>`

---

## 🏷️ Categories

### 🔸 List Categories
- **URL:** `story/categories/`
- **Method:** `GET`

---

### 🔸 Create Category (Admin Only)
- **URL:** `story/category/create`
- **Method:** `POST`
- **Headers:** `Authorization: Token <admin_token>`
- **Body:**
```form-data
name: "Adventure"
image: (optional image file)
```

---

## 💬 Comments

### 🔸 List & Add Comment to a Story
- **URL:** `story/stories/<story_id>/comment`
- **Methods:**
  - `GET` – List comments for the story
  - `POST` – Add a comment (requires auth)
- **Body (for POST):**
```json
{
  "content": "Great story!"
}
```

---

## 🧾 Notes

- Uploading images uses [ImageBB](https://imgbb.com/) under the hood.
- Protected routes require `Authorization: Token <token>` header.
- Admin-only actions are protected via `IsAdminUser`.
