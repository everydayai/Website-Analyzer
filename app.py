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
    if not url.startswith("http"):
        url = f"https://{url}"

    visited = set()
    to_visit = [url]
    all_content = []
    scrape_successful = False

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            visited.add(current_url)
            scrape_successful = True

            # Extract meaningful content
            meta_description = soup.find("meta", {"name": "description"})
            if meta_description and meta_description.get("content"):
                all_content.append(meta_description["content"])

            paragraphs = soup.find_all("p")
            for para in paragraphs:
                all_content.append(para.get_text(strip=True))

            links = soup.find_all("a", href=True)
            for link in links:
                full_url = urljoin(current_url, link["href"])
                if url in full_url and full_url not in visited:
                    to_visit.append(full_url)

        except Exception:
            # Silently skip any errors during scraping
            continue

    return " ".join(all_content[:3000]), scrape_successful

# Initial system message setup
initial_messages = [{
    "role": "system",
    "content": """You are a world-class marketing strategist trained by Neil Patel, David Ogilvy, and Seth Godin. 
    Your task is to create highly customized and innovative marketing plans based on the provided details. 
    Go beyond generic strategies and use advanced analysis to recommend:
    - Marketing tactics inspired by successful case studies from the same or similar industries.
    - Unique approaches that leverage emerging trends, tools, and platforms.
    - Recommendations that align with the business's budget and specific goals.
    Each strategy must:
    - Be actionable, with clear steps to execute.
    - Include measurable KPIs to track success.
    - Be specific to the business's industry, competitive landscape, and target audience.
    Ensure every suggestion feels fresh, creative, and deeply tailored to the business's needs."""
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

def generate_marketing_plan(website_content, industry, goals, budget, messages, fallback=False):
    """
    Generates a marketing plan based on website content, industry, and user goals.
    """
    query = f"""
    The user has provided the following details:
    - Website content: {website_content if not fallback else "N/A (website content could not be retrieved)"}
    - Industry: {industry}
    - Goals for 2025: {goals}
    - Marketing budget for 2025: ${budget}
    Create a comprehensive, customized 1-year marketing plan for 2025, including:
    - Advanced analysis based on successful case studies and trends.
    - Unique strategies for the business to stand out.
    - Actionable steps with measurable KPIs.
    Avoid generic suggestions; focus on innovative and practical ideas."""
    
    messages.append({"role": "user", "content": query})
    return call_openai_api(messages)

# Streamlit setup
st.set_page_config(layout="wide")

# Initialize session state
if "reply" not in st.session_state:
    st.session_state["reply"] = None
if "show_notice" not in st.session_state:
    st.session_state["show_notice"] = False

# Centered title
st.markdown("<h1 style='text-align: center; color: black;'>2025 Marketing Planner</h1>", unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Enter Business Details</h2>", unsafe_allow_html=True)
    website_url = st.text_input("Enter your business website", placeholder="e.g., https://example.com")
    industry = st.text_input("Industry", placeholder="E.g., Real Estate, Retail, Technology")
    goals = st.text_area("Goals for 2025", placeholder="E.g., increase brand awareness, drive online sales")
    budget = st.number_input("Marketing Budget for 2025 ($)", min_value=1000, step=1000)
    generate_button = st.button('Generate Marketing Plan')

# Process results on button click
if generate_button:
    st.session_state["show_notice"] = True
    with st.spinner("Analyzing website content and preparing your report..."):
        website_content, scrape_successful = scrape_website(website_url) if website_url else ("", False)
    fallback_mode = not scrape_successful
    if fallback_mode:
        st.warning("Unable to retrieve website content. Generating recommendations based on your input.")
    messages = initial_messages.copy()
    st.session_state["reply"] = generate_marketing_plan(
        website_content if scrape_successful else "N/A", 
        industry, goals, budget, messages, fallback=fallback_mode
    )
    st.session_state["show_notice"] = False  # Remove the notice once the report is ready

# Display the waiting notice
if st.session_state["show_notice"]:
    st.info("Generating your marketing plan. This process may take a minute or two. Please wait...")

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Your 2025 Marketing Plan ⬇️</h2>", unsafe_allow_html=True)
        st.markdown(st.session_state["reply"])
