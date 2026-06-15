# exe19_backend.py - Dedicated FastAPI backend for Streamlit UI

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from bson import ObjectId
from mongo_database import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Streamlit MongoDB API",
    version="1.0.0",
    description="Dedicated backend API for Streamlit Dashboard"
)

# Add CORS middleware to allow Streamlit to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    age: int
    created_at: datetime

class PostCreate(BaseModel):
    user_id: str
    title: str
    content: str

class PostResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    created_at: datetime

# Initialize database
db = None

@app.on_event("startup")
async def startup_event():
    global db
    try:
        db = DatabaseManager(db_name='streamlit_demo_db')
        print("✅ Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    global db
    if db:
        db.client.close()
        print("✅ MongoDB connection closed")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Streamlit MongoDB API", "status": "running"}

# Add this new endpoint for getting all posts
@app.get("/posts", response_model=List[dict])
async def get_all_posts():
    """Get all posts (for dashboard metrics)"""
    try:
        posts = list(db.posts_collection.find())
        # Convert ObjectId to string for JSON response
        for post in posts:
            post['id'] = str(post['_id'])
            post['user_id'] = str(post['user_id'])
            del post['_id']
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User endpoints
@app.post("/users", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    try:
        user_id = db.create_user(user.name, user.email, user.age)
        if user_id:
            return {"message": "User created", "user_id": user_id}
        raise HTTPException(status_code=400, detail="Email might already exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", response_model=List[UserResponse])
async def get_all_users():
    try:
        users = db.get_all_users()
        return [
            UserResponse(
                id=user['id'],
                name=user['name'],
                email=user['email'],
                age=user['age'],
                created_at=user['created_at']
            )
            for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid ID")
        
        user = db.users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "age": user['age'],
            "created_at": user['created_at']
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{user_id}")
async def update_user(user_id: str, user: UserCreate):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid ID")
        
        result = db.update_user(user_id, user.name, user.email, user.age)
        if result:
            return {"message": "User updated"}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid ID")
        
        result = db.delete_user(user_id)
        if result:
            return {"message": "User deleted"}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Post endpoints
@app.post("/posts", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    try:
        if not ObjectId.is_valid(post.user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        post_id = db.create_post(post.user_id, post.title, post.content)
        if post_id:
            return {"message": "Post created", "post_id": post_id}
        raise HTTPException(status_code=400, detail="Failed to create post")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/posts")
async def get_user_posts(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        posts = db.get_user_posts(user_id)
        return [
            {
                "id": post['id'],
                "title": post['title'],
                "content": post['content'],
                "created_at": post['created_at']
            }
            for post in posts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    try:
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        result = db.delete_post(post_id)
        if result:
            return {"message": "Post deleted"}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)