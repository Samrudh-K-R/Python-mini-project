import streamlit as st
import database
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

# Initialize database
database.init_db()

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

def add_bg_slideshow():
    # 8 High-quality images from Picsum
    images = [
        "https://picsum.photos/id/1015/3840/2160", # River
        "https://picsum.photos/id/1016/3840/2160", # Canyon
        "https://picsum.photos/id/1018/3840/2160", # Nature
        "https://picsum.photos/id/1019/3840/2160", # Tech
        "https://picsum.photos/id/1021/3840/2160", # Foggy Forest
        "https://picsum.photos/id/1022/3840/2160", # Stars
        "https://picsum.photos/id/1025/3840/2160", # Pug (cute)
        "https://picsum.photos/id/1039/3840/2160"  # Waterfall
    ]
    
    css_animation = """
    <style>
    .stApp {
        background-color: transparent;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    
    .slideshow {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: -1;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    .slideshow li {
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0;
        z-index: 0;
        animation: imageAnimation 80s linear infinite;
    }
    
    .slideshow li:nth-child(1) { background-image: url(https://picsum.photos/id/1015/3840/2160); animation-delay: 0s; }
    .slideshow li:nth-child(2) { background-image: url(https://picsum.photos/id/1016/3840/2160); animation-delay: 10s; }
    .slideshow li:nth-child(3) { background-image: url(https://picsum.photos/id/1018/3840/2160); animation-delay: 20s; }
    .slideshow li:nth-child(4) { background-image: url(https://picsum.photos/id/1019/3840/2160); animation-delay: 30s; }
    .slideshow li:nth-child(5) { background-image: url(https://picsum.photos/id/1021/3840/2160); animation-delay: 40s; }
    .slideshow li:nth-child(6) { background-image: url(https://picsum.photos/id/1022/3840/2160); animation-delay: 50s; }
    .slideshow li:nth-child(7) { background-image: url(https://picsum.photos/id/1025/3840/2160); animation-delay: 60s; }
    .slideshow li:nth-child(8) { background-image: url(https://picsum.photos/id/1039/3840/2160); animation-delay: 70s; }
    
    @keyframes imageAnimation {
        0% { opacity: 0; animation-timing-function: ease-in; }
        6% { opacity: 1; animation-timing-function: ease-out; }
        12.5% { opacity: 1; }
        18.5% { opacity: 0; }
        100% { opacity: 0; }
    }
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 32, 39, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: white !important;
    }
    </style>
    
    <ul class="slideshow">
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
    </ul>
    """
    st.markdown(css_animation, unsafe_allow_html=True)

add_bg_slideshow()

def login_signup():
    st.title("Welcome to Expense Tracker")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            # Strip whitespace to avoid errors
            username = username.strip()
            password = password.strip()
            
            user = database.check_login(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = {'username': user[0], 'name': user[2], 'age': user[3], 'job': user[4]}
                st.success(f"Welcome back, {user[2]}!")
                st.rerun()
            else:
                st.error("Invalid username or password")
                
    with tab2:
        st.subheader("Sign Up")
        new_user = st.text_input("Username", key="signup_user")
        new_pass = st.text_input("Password", type="password", key="signup_pass")
        new_name = st.text_input("Full Name")
        new_age = st.number_input("Age", min_value=0, max_value=120)
        new_job = st.text_input("Job/Profession")
        
        if st.button("Sign Up"):
            if new_user and new_pass:
                # Strip whitespace
                new_user = new_user.strip()
                new_pass = new_pass.strip()
                
                if database.create_user(new_user, new_pass, new_name, new_age, new_job):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Username already exists.")
            else:
                st.error("Please fill in all required fields.")

def main_app():
    user = st.session_state['user_info']
    
    # Sidebar Profile Section
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 80px; margin-bottom: 10px; filter: drop-shadow(0 0 10px rgba(255,215,0,0.5));">💰</div>
        <h1 style="color: white; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">Expense<br>Tracker</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"### Welcome, {user['name']}!")
    
    with st.sidebar.expander("Profile Details"):
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Age:** {user['age']}")
        st.write(f"**Job:** {user['job']}")
        
        # Edit Profile
        with st.form("edit_profile"):
            edit_name = st.text_input("Name", value=user['name'])
            edit_age = st.number_input("Age", value=user['age'] if user['age'] else 0)
            edit_job = st.text_input("Job", value=user['job'] if user['job'] else "")
            if st.form_submit_button("Update Profile"):
                database.update_user_details(user['username'], edit_name, edit_age, edit_job)
                st.session_state['user_info']['name'] = edit_name
                st.session_state['user_info']['age'] = edit_age
                st.session_state['user_info']['job'] = edit_job
                st.success("Profile updated!")
                st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_info'] = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("Add New Expense")
    
    with st.sidebar.form("add_expense_form"):
        date = st.date_input("Date")
        
        # Category suggestions with emojis
        categories = {
            "Food": "🍔",
            "Transport": "🚗",
            "Utilities": "💡",
            "Shopping": "🛍️",
            "Entertainment": "🎬",
            "Health": "💊",
            "Other": "📦"
        }
        
        category = st.selectbox("Category", list(categories.keys()))
        
        # Display category emoji/image
        st.sidebar.markdown(f"<h1 style='text-align: center;'>{categories[category]}</h1>", unsafe_allow_html=True)
        
        amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if category and amount > 0:
                # Pass user_id to add_expense
                database.add_expense(date.isoformat(), category, amount, description, user['username'])
                st.success("Expense added successfully!")
            else:
                st.error("Please enter a valid category and amount.")

    # Main content
    st.title("Dashboard")
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Recent Expenses")
        # Pass user_id to get_expenses
        expenses = database.get_expenses(user['username'])
        if expenses:
            # Convert to DataFrame for better display
            df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Category', 'Amount', 'Description', 'User ID'])
            
            # Format Amount with ₹
            df['Amount'] = df['Amount'].apply(lambda x: f"₹{x:.2f}")
            
            # Drop ID and User ID for display
            st.dataframe(df.drop(['ID', 'User ID'], axis=1), width='stretch')
        else:
            st.info("No expenses found.")

    with col2:
        st.subheader("Expenses by Category")
        # Pass user_id to get_expenses_by_category
        category_data = database.get_expenses_by_category(user['username'])
        if category_data:
            import plotly.express as px
            
            # Create interactive pie chart with Plotly
            df_cat = pd.DataFrame(category_data, columns=['Category', 'Amount'])
            
            fig = px.pie(df_cat, values='Amount', names='Category', 
                         title='Expenses by Category',
                         hover_data=['Amount'],
                         labels={'Amount':'Amount (₹)'})
            
            # Update traces to show labels and arrows
            fig.update_traces(textposition='outside', textinfo='label+percent')
            
            # Optimize layout for smaller spaces
            fig.update_layout(
                margin=dict(l=40, r=40, t=40, b=40),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data to display.")

# App Flow Control
if st.session_state['logged_in']:
    main_app()
else:
    login_signup()
