import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

def scrape_website(url):
    """
    Scrapes the given website URL to extract business-related information.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract meta description or a paragraph as a summary
        description = soup.find("meta", {"name": "description"}) or soup.find("p")
        return description.get("content") if description else "No description found."
    except Exception as e:
        return f"Error fetching website data: {e}"

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )

def CustomChatGPT(home_size, stories, paint_type, paint_cost, labor_cost, business_info, messages):
    query = f"""
    The user has provided the following details:
    - Square footage: {home_size} sqft
    - Number of stories: {stories}
    - Painting type requested: {paint_type}
    - Paint cost per gallon: ${paint_cost}
    - Labor cost per hour: ${labor_cost}
    
    Additional business information: {business_info}
    
    Provide a detailed cost estimate to paint the home, factoring in the user-specified paint 
    and labor costs. Include a breakdown for labor, materials, and other expenses. Provide insights 
    on any factors that might affect the cost.
    """
    
    messages.append({"role": "user", "content": query})
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Streamlit setup
st.set_page_config(layout="wide")

# Initialize session state
if "reply" not in st.session_state:
    st.session_state["reply"] = None

# Centered title
st.markdown("<h1 style='text-align: center; color: black;'>Home Painting Cost Estimator with Business Info</h1>", unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Enter Home and Cost Details</h2>", unsafe_allow_html=True)
    home_size = st.number_input("Square Footage of Home", min_value=100, max_value=10000, step=50)
    stories = st.selectbox("Number of Stories", options=["1", "2", "3"])
    paint_type = st.selectbox("Type of Painting", options=["Interior", "Exterior", "Both"])
    paint_cost = st.number_input("Cost of Paint per Gallon ($)", min_value=1.0, step=0.5)
    labor_cost = st.number_input("Labor Cost per Hour ($)", min_value=1.0, step=0.5)
    website_url = st.text_input("Enter your business website (optional)", placeholder="https://example.com")
    generate_button = st.button('Estimate Painting Cost')

# Process results on button click
if generate_button:
    business_info = scrape_website(website_url) if website_url else "No additional business information provided."
    messages = [{
        "role": "system",
        "content": """
        You are a detailed home painting cost estimator. Based on provided home details 
        and optional business information, generate a comprehensive cost estimate. 
        Include a breakdown for labor, materials, and other expenses, factoring in any 
        user-provided costs. Offer insights on factors that might affect pricing.
        """
    }]
    st.session_state["reply"], _ = CustomChatGPT(home_size, stories, paint_type, paint_cost, labor_cost, business_info, messages)

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Estimated Painting Cost ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
