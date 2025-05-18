import streamlit as st
from PIL import Image
import os
import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(layout="wide", page_title="📊 Bank Customer Churn Dashboard")

# Custom CSS styling
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; padding: 10px 30px; }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
        }
        .st-expanderHeader {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with user input form
with st.sidebar:
    st.header("🔐 User Details (Required)")
    with st.form(key='user_form'):
        user_name = st.text_input("Full Name", placeholder="Enter your name")
        user_email = st.text_input("Email Address", placeholder="Enter your email")
        submitted = st.form_submit_button("Submit")

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    if not submitted:
        st.sidebar.info("ℹ️ Please fill out the form and press Submit.")
        st.stop()
    elif not user_name or not user_email:
        st.sidebar.warning("⚠️ Both Name and Email are required to proceed.")
        st.stop()
    elif not re.match(email_pattern, user_email.strip()):
        st.sidebar.error("❌ Invalid Email Format. Please enter a valid email like `example@domain.com`.")
        st.stop()
    else:
        st.sidebar.success("✅ Details submitted successfully!")

# Function to save user info
def save_user_info(user_name, user_email, file_path="data/user_info.csv"):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Email'])
        writer.writerow([user_name, user_email])

# Save user info
save_user_info(user_name, user_email)

# Load dataset
data_path = "data/Bank Customer Churn Prediction.csv"
if not os.path.exists(data_path):
    st.error("❌ Dataset file not found. Please ensure 'Bank Customer Churn Prediction.csv' is in the 'data/' directory.")
    st.stop()
df = pd.read_csv(data_path)

# Create plots directory
plot_dir = "plots"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Function to save plots
def save_plot(fig, filename):
    filepath = os.path.join(plot_dir, filename)
    fig.savefig(filepath, bbox_inches='tight')
    plt.close(fig)
    return filepath

# Generate visualizations
# 1. Churn Rate Pie Chart
churn_counts = df['churn'].value_counts(normalize=True) * 100
fig1, ax1 = plt.subplots()
ax1.pie(churn_counts, labels=['Retained', 'Churned'], autopct='%1.2f%%', colors=['#66b3ff', '#ff9999'])
ax1.set_title("Churn Rate")
pie_chart_path = save_plot(fig1, "churn_distribution.png")

# 2. Churn by Country
fig2, ax2 = plt.subplots()
sns.barplot(x='country', y='churn', data=df, estimator=lambda x: sum(x)/len(x)*100, ax=ax2)
ax2.set_title("Churn Rate by Country")
ax2.set_ylabel("Churn Rate (%)")
country_chart_path = save_plot(fig2, "churn_rate_by_country.png")

# 3. Churn by Age Group
df['age_group'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 100], labels=['<30', '30-40', '40-50', '50+'])
fig3, ax3 = plt.subplots()
sns.barplot(x='age_group', y='churn', data=df, estimator=lambda x: sum(x)/len(x)*100, ax=ax3)
ax3.set_title("Churn Rate by Age Group")
ax3.set_ylabel("Churn Rate (%)")
age_chart_path = save_plot(fig3, "churn_by_age.png")

# 4. Churn by Active Member
fig4, ax4 = plt.subplots()
sns.barplot(x='active_member', y='churn', data=df, estimator=lambda x: sum(x)/len(x)*100, ax=ax4)
ax4.set_title("Churn Rate by Active Member Status")
ax4.set_xticklabels(['Inactive', 'Active'])
ax4.set_ylabel("Churn Rate (%)")
active_chart_path = save_plot(fig4, "churn_by_active_member.png")

# 5. Estimated Salary Distribution
fig5, ax5 = plt.subplots()
sns.histplot(df['estimated_salary'], kde=True, ax=ax5)
ax5.set_title("Estimated Salary Distribution")
ax5.set_xlabel("Estimated Salary")
salary_chart_path = save_plot(fig5, "estimated_salary.png")

# Dashboard title and welcome message
st.title("📊 Bank Customer Churn Dashboard")
st.markdown(f"""
**👋 Welcome, `{user_name}`!**

Explore key insights into bank customer churn through interactive visualizations. Analyze churn patterns by demographics, engagement, and financial metrics to inform retention strategies.
""")

# About section
with st.expander("📘 About This Dashboard", expanded=True):
    st.markdown("""
    **Dataset**: Bank Customer Churn Prediction  \n
    **Records**: 10,000 customers  \n
    **Features Analyzed**: Credit Score, Country, Gender, Age, Tenure, Balance, Products Number, Credit Card, Active Member, Estimated Salary, Churn  \n
    **Objective**: Identify factors driving customer churn and visualize patterns for strategic insights  \n
    ---
    This dashboard provides a data-driven view of churn behavior using visualizations like churn rate, demographic breakdowns, and salary distributions.  \n
    📊 Use it to uncover high-risk customer segments and guide retention efforts.  \n
    ---
    ⚠️ **Note**: This is an evolving project. Features and accuracy are continuously being improved.
    """)

# Tabs for analysis
tab1, tab2 = st.tabs(["📈 Churn Analysis", "📊 Summary Statistics"])

# Tab 1: Churn Analysis
with tab1:
    st.subheader("📈 Churn Patterns and Insights")
    def display_chart(title, image_path, pattern, interpretation):
        with st.container():
            st.subheader(title)
            col1, col2 = st.columns([2, 3])
            if os.path.exists(image_path):
                with col1:
                    st.image(Image.open(image_path), use_container_width=True)
            else:
                with col1:
                    st.warning(f"⚠️ Image not found: `{image_path}`")
            with col2:
                st.markdown(f"**🔍 Pattern Observed:** {pattern}")
                st.markdown(f"**💡 Interpretation:** {interpretation}")
            st.markdown("—" * 30)

    charts_info = [
        ("1️⃣ Overall Churn Rate", pie_chart_path,
         "Approximately 20.37% of customers churned, while 79.63% remained.",
         "The churn rate indicates a significant portion of customers are leaving, warranting targeted retention strategies. Focus on understanding the characteristics of the 20.37% who churned."),

        ("2️⃣ Churn by Country", country_chart_path,
         "Churn rates vary across countries, with potential differences in France, Spain, and Germany.",
         "Higher churn in specific countries (e.g., Germany) may reflect regional service issues or market competition. Investigate country-specific factors to reduce churn."),

        ("3️⃣ Churn by Age Group", age_chart_path,
         "Older age groups (e.g., 50+) may exhibit higher churn rates compared to younger groups.",
         "Older customers are at higher risk of churning, possibly due to life stage changes or dissatisfaction. Tailor engagement strategies for older segments."),

        ("4️⃣ Churn by Active Member Status", active_chart_path,
         "Inactive members have a significantly higher churn rate than active members.",
         "Engagement is a key predictor of retention. Inactive customers should be targeted with re-engagement campaigns to reduce churn."),

        ("5️⃣ Estimated Salary Distribution", salary_chart_path,
         "Salaries are roughly uniformly distributed, with no distinct clusters.",
         "Salary alone may not drive churn, but combining it with other features (e.g., balance or products) could reveal high-risk segments.")
    ]

    for title, filename, pattern, interpretation in charts_info:
        display_chart(title, filename, pattern, interpretation)

# Tab 2: Summary Statistics
with tab2:
    st.subheader("📊 Dataset Summary Statistics")
    with st.expander("📊 Summary Statistics", expanded=True):
        st.markdown("### Dataset Overview")
        st.write(df.describe())
        st.markdown("### Churn Rate")
        churn_rate = df['churn'].value_counts(normalize=True) * 100
        st.write(churn_rate.rename({0: 'Retained', 1: 'Churned'}))
        st.markdown("### Key Insights")
        st.markdown("""
        - **Churn Rate**: ~20.37% of customers churned, indicating a need for retention strategies.
        - **Age**: Average age is ~38.9 years, with a wide range (18–92), suggesting age-related churn patterns.
        - **Balance**: Many customers have zero balance, potentially indicating inactivity.
        - **Active Members**: Likely lower churn among active members, highlighting the importance of engagement.
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "📧 Contact: support@bankchurn.com | "
    "© 2025 Bank Churn Analysis Dashboard |"
    "👤 Developed by Abhishek Singh Dikhit"
    "</div>", unsafe_allow_html=True)

st.balloons()
st.success("✅ Dashboard Loaded Successfully! Explore the charts to uncover churn patterns and insights.")