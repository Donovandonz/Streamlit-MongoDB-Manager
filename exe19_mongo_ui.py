# exe19_mongo_ui.py - MongoDB Database Manager UI

import streamlit as st
import requests
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="MongoDB Database Manager",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL (make sure your FastAPI server is running on this port)
API_BASE_URL = "http://localhost:8002"

# ========== API FUNCTIONS ==========
def check_api_connection():
    """Check if the FastAPI server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        return response.status_code == 200
    except requests.RequestException:
        return False

def create_user(name, email, age):
    """Create a new user via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/users",
            json={"name": name, "email": email, "age": age}
        )
        return response.json(), response.status_code == 201
    except Exception as e:
        return {"error": str(e)}, False

def get_all_users():
    """Get all users via API"""
    try:
        response = requests.get(f"{API_BASE_URL}/users")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception:
        return [], False

def get_user_posts(user_id):
    """Get posts for a specific user"""
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/posts")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception:
        return [], False

def create_post(user_id, title, content):
    """Create a new post via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/posts",
            json={"user_id": user_id, "title": title, "content": content}
        )
        return response.json(), response.status_code == 201
    except Exception as e:
        return {"error": str(e)}, False

def get_all_posts():
    """Get all posts via API"""
    try:
        response = requests.get(f"{API_BASE_URL}/posts")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception:
        return [], False

def delete_user(user_id):
    """Delete a user via API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/users/{user_id}")
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def delete_post(post_id):
    """Delete a post via API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/posts/{post_id}")
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def update_user(user_id, name, email, age):
    """Update a user via API"""
    try:
        response = requests.put(
            f"{API_BASE_URL}/users/{user_id}",
            json={"name": name, "email": email, "age": age}
        )
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

# ========== UI PAGES ==========
def dashboard_page():
    """Main dashboard with metrics"""
    st.header("📊 Dashboard")
    
    # Get data for dashboard
    users, users_success = get_all_users()
    posts, posts_success = get_all_posts()
    
    if users_success and posts_success:
        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Users", len(users))
        
        with col2:
            st.metric("📝 Total Posts", len(posts))
        
        with col3:
            avg_age = sum(user['age'] for user in users) / len(users) if users else 0
            st.metric("📅 Average Age", f"{avg_age:.1f}")
        
        with col4:
            posts_per_user = len(posts) / len(users) if users else 0
            st.metric("📊 Posts per User", f"{posts_per_user:.1f}")
        
        st.markdown("---")
        
        # Display recent users
        st.subheader("📋 Recent Users")
        if users:
            df = pd.DataFrame(users)
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df[['id', 'name', 'email', 'age', 'created_at']], use_container_width=True)
        else:
            st.info("No users found. Create your first user!")
        
        # Display recent posts
        st.subheader("📝 Recent Posts")
        if posts:
            df_posts = pd.DataFrame(posts)
            if 'created_at' in df_posts.columns:
                df_posts['created_at'] = pd.to_datetime(df_posts['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df_posts[['id', 'user_id', 'title', 'content', 'created_at']], use_container_width=True)
        else:
            st.info("No posts found. Create your first post!")
    else:
        st.error("Failed to fetch data from API")

def users_page():
    """Manage users"""
    st.header("👥 User Management")
    
    tab1, tab2, tab3 = st.tabs(["➕ Create User", "📋 View Users", "✏️ Update/Delete"])
    
    # Tab 1: Create User
    with tab1:
        with st.form("create_user_form"):
            st.subheader("Create New User")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name *")
                email = st.text_input("Email *")
            with col2:
                age = st.number_input("Age", min_value=1, max_value=120, value=25)
            
            submitted = st.form_submit_button("🚀 Create User", type="primary")
            
            if submitted:
                if name and email:
                    with st.spinner("Creating user..."):
                        result, success = create_user(name, email, age)
                        if success:
                            st.success(f"✅ User '{name}' created successfully!")
                            st.info(f"📌 User ID: {result.get('user_id')}")
                        else:
                            st.error(f"❌ Failed to create user: {result.get('detail', 'Unknown error')}")
                else:
                    st.warning("Please fill in all required fields (*)")
    
    # Tab 2: View Users
    with tab2:
        st.subheader("All Users")
        with st.spinner("Loading users..."):
            users, success = get_all_users()
        
        if success and users:
            # Search filter
            search = st.text_input("🔍 Search users by name or email", "")
            if search:
                users = [u for u in users if search.lower() in u['name'].lower() or search.lower() in u['email'].lower()]
            
            df = pd.DataFrame(users)
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df[['id', 'name', 'email', 'age', 'created_at']], use_container_width=True)
            st.caption(f"📊 Total: {len(users)} users")
        else:
            st.info("No users found")
    
    # Tab 3: Update/Delete User
    with tab3:
        with st.spinner("Loading users..."):
            users, success = get_all_users()
        
        if success and users:
            user_options = {f"{user['name']} ({user['email']})": user['id'] for user in users}
            selected_user_display = st.selectbox("Select User to manage", list(user_options.keys()))
            
            if selected_user_display:
                user_id = user_options[selected_user_display]
                selected_user = next(u for u in users if u['id'] == user_id)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.form("update_user_form"):
                        st.subheader("✏️ Update User")
                        new_name = st.text_input("Name", value=selected_user['name'])
                        new_email = st.text_input("Email", value=selected_user['email'])
                        new_age = st.number_input("Age", value=selected_user['age'], min_value=1, max_value=120)
                        
                        if st.form_submit_button("💾 Update User"):
                            with st.spinner("Updating user..."):
                                result, success = update_user(user_id, new_name, new_email, new_age)
                                if success:
                                    st.success("✅ User updated successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed: {result.get('detail', 'Unknown error')}")
                
                with col2:
                    st.subheader("🗑️ Delete User")
                    st.warning(f"⚠️ This will delete **{selected_user['name']}** AND **all their posts**! This action cannot be undone.")
                    if st.button("🗑️ Delete User", type="primary"):
                        with st.spinner("Deleting user..."):
                            result, success = delete_user(user_id)
                            if success:
                                st.success("✅ User deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"❌ Failed: {result.get('detail', 'Unknown error')}")
        else:
            st.info("No users to manage")

def posts_page():
    """Manage posts"""
    st.header("📝 Post Management")
    
    tab1, tab2 = st.tabs(["➕ Create Post", "📋 View Posts"])
    
    # Tab 1: Create Post
    with tab1:
        with st.spinner("Loading users..."):
            users, users_success = get_all_users()
        
        if users_success and users:
            user_options = {f"{user['name']} ({user['email']})": user['id'] for user in users}
            selected_user = st.selectbox("Select User", list(user_options.keys()))
            
            with st.form("create_post_form"):
                title = st.text_input("Title *")
                content = st.text_area("Content *", height=150)
                
                if st.form_submit_button("📝 Create Post", type="primary"):
                    if title and content:
                        with st.spinner("Creating post..."):
                            user_id = user_options[selected_user]
                            result, success = create_post(user_id, title, content)
                            if success:
                                st.success("✅ Post created successfully!")
                            else:
                                st.error(f"❌ Failed: {result.get('detail', 'Unknown error')}")
                    else:
                        st.warning("Please fill in all fields")
        else:
            st.info("No users found. Create a user first!")
    
    # Tab 2: View Posts by User
    with tab2:
        with st.spinner("Loading users..."):
            users, users_success = get_all_users()
        
        if users_success and users:
            user_options = {f"{user['name']} ({user['email']})": user['id'] for user in users}
            selected_user_display = st.selectbox("Select User to view posts", list(user_options.keys()))
            
            if selected_user_display:
                user_id = user_options[selected_user_display]
                
                with st.spinner("Loading posts..."):
                    posts, success = get_user_posts(user_id)
                
                if success and posts:
                    st.subheader(f"📌 Posts by {selected_user_display}")
                    for post in posts:
                        with st.expander(f"📄 {post['title']}"):
                            st.write(f"**Content:** {post['content']}")
                            st.write(f"**Created:** {pd.to_datetime(post['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
                            
                            if st.button("🗑️ Delete", key=f"delete_{post['id']}"):
                                with st.spinner("Deleting post..."):
                                    result, success = delete_post(post['id'])
                                    if success:
                                        st.success("✅ Post deleted!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete")
                else:
                    st.info("No posts found for this user")
        else:
            st.info("No users found")

# ========== MAIN APP ==========
# ========== MAIN APP ==========
def main():
    st.title("🗄️ MongoDB Database Manager")
    st.markdown("*A web interface for managing your MongoDB database via FastAPI*")
    
    # Check API connection
    with st.spinner("Checking connection to FastAPI server..."):
        if not check_api_connection():
            st.error("❌ Cannot connect to FastAPI server!")
            st.info("""
            **To fix this issue:**
            1. Open a new terminal
            2. Navigate to your exe19 folder
            3. Run `python exe19_backend.py`
            4. Keep that terminal running
            5. Refresh this page
            
            The API server must be running on port 8002
            """)
            return
    
    st.success("✅ Connected to FastAPI server on port 8002!")
    
    # Sidebar navigation
    st.sidebar.title("📂 Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Go to",
        ["📊 Dashboard", "👥 Users", "📝 Posts"],
        format_func=lambda x: x
    )
    
    # Display selected page
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "👥 Users":
        users_page()
    elif page == "📝 Posts":
        posts_page()
    
    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**System Requirements:**\n"
        "- ✅ FastAPI server running on port 8002\n"
        "- ✅ MongoDB Atlas connection configured\n"
        "- ✅ Run `python exe19_backend.py` to start the API\n\n"
        "**API Endpoints:**\n"
        "- GET /users\n"
        "- POST /users\n"
        "- GET /users/{id}/posts\n"
        "- DELETE /users/{id}\n"
        "- POST /posts\n"
        "- GET /posts\n"
        "- DELETE /posts/{id}"
    )

if __name__ == "__main__":
    main()