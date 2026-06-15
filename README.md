# Streamlit-MongoDB-Manager
## 🗄️ MongoDB Manager - Full Stack Portfolio Project

A complete full-stack application for managing MongoDB databases, built with **FastAPI**, **Streamlit**, and **MongoDB Atlas**.

---

## 🚀 Features

### Backend API (FastAPI)
- Full CRUD operations for users and posts
- RESTful endpoints with Swagger documentation
- MongoDB Atlas connection
- CORS enabled for frontend communication

### Frontend UI (Streamlit)
- **Dashboard**: View metrics (total users, posts, avg age)
- **User Management**: Create, read, update, delete users
- **Post Management**: Create posts, view by user, delete posts
- **Personal Dashboard**: Interactive demo with save-to-database feature

### Technologies Used
| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Database | MongoDB Atlas (Cloud) |
| Data Validation | Pydantic |
| HTTP Client | Requests |

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| GET | `/users` | Get all users |
| POST | `/users` | Create user |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |
| GET | `/posts` | Get all posts |
| POST | `/posts` | Create post |
| GET | `/users/{id}/posts` | Get user's posts |
| DELETE | `/posts/{id}` | Delete post |

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB Atlas account (free tier)
- Git

## AND Install this requirement.txt:
```
pip install -r requirements.txt
```

---

## 🚀 Running the Application

Terminal 1: Start Backend (Server runs on http://localhost:8002)
```
python exe19_backend.py
```

Terminal 2: Start Frontend (App opens at http://localhost:8501)
```
streamlit run exe19_mongo_ui.py
```

Optional: Personal Dashboard
```
streamlit run exe19_dashboard.py --server.port 8502
```

---

# 🏗️ Framework Structure
```mermaid
flowchart LR
    A[Browser] -->|1. User clicks| B[Streamlit]
    B -->|2. HTTP Request| C[FastAPI]
    C -->|3. Query| D[MongoDB]
    D -->|4. JSON| C
    C -->|5. Response| B
    B -->|6. Display| A

    style A fill:#61DAFB,color:#000
    style B fill:#47A248,color:#fff
    style C fill:#FFD700,color:#000
    style D fill:#00BFFF,color:#fff
```
---

# UI Overview

<img width="1906" height="917" alt="Screenshot 2026-06-15 125347" src="https://github.com/user-attachments/assets/d73e1a20-67da-4fe0-a25b-0eaae19fd1a2" />

<img width="1912" height="905" alt="Screenshot 2026-06-15 125659" src="https://github.com/user-attachments/assets/bd25a0cd-f272-40f8-b1e5-229d1959e13f" />

<img width="1910" height="923" alt="Screenshot 2026-06-15 125744" src="https://github.com/user-attachments/assets/6ae482d2-772f-4632-a8b0-7f260ec18003" />








