import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def scrape_website(url):
    """
    Scrapes the given website URL to extract business-related information.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract meta description or the first paragraph as a summary
        description = soup.find("meta", {"name": "description"})
        if description and description.get("content"):
            return description["content"]
        else:
            paragraph = soup.find("p")
            return paragraph.get_text(strip=True) if paragraph else "No description found."
    except Exception as e:
        return f"Error fetching website data: {e}"

def call_openai_api(prompt):
    """
    Calls the OpenAI API using the updated interface for synchronous requests.
    """
    response = openai.Completion.create(
        model="text-davinci-003",  # Replace with your desired model
        prompt=prompt,
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def generate_marketing_plan(website_info, industry, goals, budget):
    """
    Generates a marketing plan based on website information, industry, and user goals.
    """
    prompt = f"""
    The user has provided the following details:
    - Website information: {website_info}
    - Industry: {industry}
    - Goals for 2025: {goals}
    - Marketing budget for 2025: ${budget}
    
    Please create a comprehensive marketing plan for 2025. Include specific strategies 
    (e.g., content marketing, social media, advertising, SEO) and a timeline for implementing them.
    Highlight how the website's strengths can be leveraged to achieve the stated goals.
    """
    
    return call_openai_api(prompt)

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
    website_url = st.text_input("Enter your business website", placeholder="https://example.com")
    industry = st.text_input("Industry", placeholder="E.g., Real Estate, Retail, Technology")
    goals = st.text_area("Goals for 2025", placeholder="E.g., increase brand awareness, drive online sales, expand audience")
    budget = st.number_input("Marketing Budget for 2025 ($)", min_value=1000, step=1000)
    generate_button = st.button('Generate Marketing Plan')

# Process results on button click
if generate_button and website_url:
    website_info = scrape_website(website_url)
    if "Error" not in website_info:
        st.session_state["reply"] = generate_marketing_plan(website_info, industry, goals, budget)
    else:
        st.session_state["reply"] = website_info

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Your 2025 Marketing Plan ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
