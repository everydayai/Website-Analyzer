import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def scrape_website(url, max_pages=5):
    """
    Crawls and scrapes content from the given website URL.
    Follows internal links and extracts meaningful information from up to `max_pages` pages.
    """
    # Ensure URL has the correct format
    if not url.startswith("http"):
        url = f"https://{url}"

    visited = set()
    to_visit = [url]
    all_content = []

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            visited.add(current_url)

            # Extract meaningful content (e.g., meta description, main text)
            meta_description = soup.find("meta", {"name": "description"})
            if meta_description and meta_description.get("content"):
                all_content.append(meta_description["content"])

            # Extract main text (e.g., headers, paragraphs)
            paragraphs = soup.find_all("p")
            for para in paragraphs:
                all_content.append(para.get_text(strip=True))

            # Extract internal links
            links = soup.find_all("a", href=True)
            for link in links:
                full_url = urljoin(current_url, link["href"])
                if url in full_url and full_url not in visited:
                    to_visit.append(full_url)

        except Exception as e:
            st.warning(f"Error fetching {current_url}: {e}")

    return " ".join(all_content[:3000])  # Limit content length for OpenAI API

# Initial system message setup
initial_messages = [{
    "role": "system",
    "content": """You are a world-class marketing strategist trained by Neil Patel, David Ogilvy, and Seth Godin. 
    You specialize in creating precise, highly actionable, and detailed 1-year marketing plans tailored to businesses' specific needs. 
    For every strategy you suggest, include:
    - Lists of specific keywords for blogs, videos, or SEO.
    - Titles and topics for YouTube videos, blog posts, or other content.
    - Ad campaign structures, including target audiences and platforms.
    - Step-by-step implementation details for each suggestion.
    - Measurable KPIs or success metrics.

    Your advice must be execution-ready, requiring minimal further planning by the business owner. 
    Leverage the website information provided to deeply customize your suggestions, ensuring alignment with the business's goals and strengths."""
}]

def call_openai_api(messages):
    """
    Calls the OpenAI ChatCompletion API with the correct format.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=3000,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

def generate_marketing_plan(website_content, industry, goals, budget, messages):
    """
    Generates a marketing plan based on website content, industry, and user goals.
    """
    query = f"""
    The user has provided the following details:
    - Website content: {website_content}
    - Industry: {industry}
    - Goals for 2025: {goals}
    - Marketing budget for 2025: ${budget}

    Create a comprehensive, customized 1-year marketing plan for 2025. 
    Include:
    1. **Keywords**: Provide a list of specific keywords to target for blogs, videos, and SEO.
    2. **Content Topics**: Suggest blog and YouTube video topics with detailed titles.
    3. **Social Media**: Recommend platforms, posting frequency, and campaign ideas with measurable goals.
    4. **Advertising Campaigns**: Outline paid ad strategies, including platforms, target audiences, and budget allocation.
    5. **SEO Improvements**: Suggest tools, techniques, and steps to improve search rankings.
    6. **Execution Steps**: Provide actionable, step-by-step instructions for each recommendation.

    Ensure all suggestions align with the business's goals and strengths, and include a quarterly timeline for implementation."""
    
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
    website_url = st.text_input("Enter your business website", placeholder="example.com (no need for https://)")
    industry = st.text_input("Industry", placeholder="E.g., Real Estate, Retail, Technology")
    goals = st.text_area("Goals for 2025", placeholder="E.g., increase brand awareness, drive online sales")
    budget = st.number_input("Marketing Budget for 2025 ($)", min_value=1000, step=1000)
    generate_button = st.button('Generate Marketing Plan')

# Process results on button click
if generate_button and website_url:
    with st.spinner("Analyzing website content..."):
        website_content = scrape_website(website_url)
    if website_content:
        messages = initial_messages.copy()
        st.session_state["reply"] = generate_marketing_plan(website_content, industry, goals, budget, messages)
    else:
        st.warning("Unable to retrieve website content. Please check the URL or try again.")

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Your 2025 Marketing Plan ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
