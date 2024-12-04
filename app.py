import streamlit as st
import openai
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initial system message setup
initial_messages = [{
    "role": "system",
    "content": "You are a marketing strategist who creates detailed yearly plans based on provided inputs."
}]

def call_openai_api(messages):
    """
    Calls the OpenAI ChatCompletion API with the correct format.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Ensure you're using the correct model
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

def generate_marketing_plan(website_info, industry, goals, budget, messages):
    """
    Generates a marketing plan based on website information, industry, and user goals.
    """
    query = f"""
    The user has provided the following details:
    - Website information: {website_info}
    - Industry: {industry}
    - Goals for 2025: {goals}
    - Marketing budget for 2025: ${budget}

    Create a comprehensive marketing plan for 2025. Include specific strategies 
    (e.g., content marketing, social media, advertising, SEO) and a timeline for implementing them.
    Highlight how the website's strengths can be leveraged to achieve the stated goals.
    """
    
    messages.append({"role": "user", "content": query})
    return call_openai_api(messages)

# Streamlit setup
st.set_page_config(layout="wide")

# Initialize session state
if "reply" not in st.session_state:
    st.session_state["reply"] = None

# Centered title
st.markdown("<h1 style='text-align: center; color: black;'>2025 Marketing Planner</h1>", unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Enter Business Details</h2>", unsafe_allow_html=True)
    website_info = st.text_input("Website Information", placeholder="Provide key details or a URL")
    industry = st.text_input("Industry", placeholder="E.g., Real Estate, Retail, Technology")
    goals = st.text_area("Goals for 2025", placeholder="E.g., increase brand awareness, drive online sales")
    budget = st.number_input("Marketing Budget for 2025 ($)", min_value=1000, step=1000)
    generate_button = st.button('Generate Marketing Plan')

# Process results on button click
if generate_button and website_info:
    messages = initial_messages.copy()
    st
