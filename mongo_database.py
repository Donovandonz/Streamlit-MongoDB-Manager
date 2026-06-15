# mongo_database.py - SIMPLIFIED WORKING VERSION

from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get connection string - MUST be from .env
MONGODB_URI = os.getenv('MONGODB_ATLAS_CLUSTER_URI')

if not MONGODB_URI:
    print("❌ ERROR: MONGODB_ATLAS_CLUSTER_URI not found in .env file")
    print("   Please check your .env file in:", os.getcwd())
    raise Exception("Missing MongoDB connection string")

print(f"✅ Loaded connection string (first 40 chars): {MONGODB_URI[:40]}...")


class DatabaseManager:
    def __init__(self, db_name='example_db'):
        # Use the connection string from .env
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[db_name]
        self.users_collection = self.db.users
        self.posts_collection = self.db.posts
        self.init_database()

    def init_database(self):
        """Create indexes for better performance"""
        try:
            self.users_collection.create_index("email", unique=True)
            self.posts_collection.create_index("user_id")
            print("✅ Database indexes created successfully")
        except Exception as e:
            print(f"Note: {e}")

    def create_user(self, name, email, age):
        """Create a new user"""
        try:
            user_doc = {
                "name": name,
                "email": email,
                "age": int(age),
                "created_at": datetime.now()
            }
            result = self.users_collection.insert_one(user_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def create_post(self, user_id, title, content):
        """Create a new post for a user"""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            post_doc = {
                "user_id": user_object_id,
                "title": title,
                "content": content,
                "created_at": datetime.now()
            }
            result = self.posts_collection.insert_one(post_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating post: {e}")
            return None

    def get_all_users(self):
        """Get all users"""
        try:
            users = list(self.users_collection.find())
            for user in users:
                user['id'] = str(user['_id'])
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    def get_user_posts(self, user_id):
        """Get all posts by a specific user"""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            posts = list(self.posts_collection.find(
                {"user_id": user_object_id}
            ).sort("created_at", -1))

            for post in posts:
                post['id'] = str(post['_id'])
                post['user_id'] = str(post['user_id'])
            return posts
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []

    def delete_user(self, user_id):
        """Delete a user and all their posts"""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            self.posts_collection.delete_many({"user_id": user_object_id})
            result = self.users_collection.delete_one({"_id": user_object_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def delete_post(self, post_id):
        """Delete a single post by ID"""
        try:
            if ObjectId.is_valid(post_id):
                post_object_id = ObjectId(post_id)
            else:
                post_object_id = post_id

            result = self.posts_collection.delete_one({"_id": post_object_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False

    def update_user(self, user_id, name=None, email=None, age=None):
        """Update user information"""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            updates = {}
            if name is not None:
                updates["name"] = name
            if email is not None:
                updates["email"] = email
            if age is not None:
                updates["age"] = int(age)

            if not updates:
                return False

            result = self.users_collection.update_one(
                {"_id": user_object_id},
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False