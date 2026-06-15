# Personal Dashboard with MongoDB Save Feature

import streamlit as st
import datetime
import requests

# Configure the page (MUST be first Streamlit command)
st.set_page_config(
    page_title="Personal Dashboard",
    page_icon="🌟",
    layout="centered"
)

# API base URL
API_BASE_URL = "http://localhost:8002"

# Title
st.title("🌟 Personal Dashboard")

# Sidebar for inputs
st.sidebar.header("📝 Personal Information")

name = st.sidebar.text_input("Your Name")
age = st.sidebar.number_input("Your Age", min_value=1, max_value=120, value=25)
favorite_color = st.sidebar.color_picker("Favorite Color", "#FF6B6B")
hobbies = st.sidebar.multiselect(
    "Your Hobbies",
    ["Reading", "Gaming", "Sports", "Music", "Cooking", "Travel", "Photography", "Coding"],
    default=["Reading"]
)

# ========== SAVE BUTTON (NOW AFTER VARIABLES ARE DEFINED) ==========
if name:
    if st.button("💾 Save to Database"):
        try:
            response = requests.post(
                f"{API_BASE_URL}/users",
                json={"name": name, "email": f"{name.lower().replace(' ', '.')}@example.com", "age": age}
            )
            if response.status_code == 201:
                st.success(f"✅ {name} saved to MongoDB successfully!")
                st.info(f"📌 User ID: {response.json().get('user_id')}")
            else:
                st.error(f"❌ Failed to save: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Connection error: {e}. Make sure backend is running on port 8002")

# Main content
if name:
    st.header(f"👋 Welcome, {name}!")
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎂 Age", f"{age} years")
    
    with col2:
        st.metric("🎯 Hobbies", len(hobbies))
    
    with col3:
        birth_year = datetime.datetime.now().year - age
        st.metric("📅 Birth Year", birth_year)
    
    # Display favorite color
    st.subheader("🎨 Your Favorite Color")
    st.color_picker("", favorite_color, disabled=True)
    st.markdown(f"<div style='background-color: {favorite_color}; padding: 20px; border-radius: 10px;'></div>", unsafe_allow_html=True)
    
    # Display hobbies
    if hobbies:
        st.subheader("🎯 Your Hobbies")
        cols = st.columns(len(hobbies))
        for i, hobby in enumerate(hobbies):
            with cols[i]:
                st.success(f"📌 {hobby}")
    
    # Fun fact
    st.subheader("✨ Fun Fact")
    days_lived = age * 365
    hours_lived = days_lived * 24
    st.info(f"🎉 You've lived approximately **{days_lived:,} days** or **{hours_lived:,} hours**!")
    
    # Progress bar (age percentage of 100)
    st.subheader("📊 Life Progress")
    st.progress(min(age / 100, 1.0))
    st.caption(f"You're {age}% through a 100-year journey!")
    
else:
    st.info("👈 Please enter your name in the sidebar to get started!")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")