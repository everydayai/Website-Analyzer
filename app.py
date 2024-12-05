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
    For every strategy you suggest, include 3 to 5 detailed, actionable steps that explain how to implement it. 
    Ensure each plan considers the business's industry, budget, goals, and current strengths as reflected in the provided information.

    Your advice should feel like it is coming from a personal consultant who deeply understands the business. Go beyond generalities, 
    and include specific suggestions for platforms, tools, campaigns, or techniques. If applicable, suggest measurable KPIs to track success.
    If the company is already doing well in some areas, suggest how they can take those efforts to the next level."""
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

    Based on this information, create a comprehensive, customized 1-year marketing plan for 2025. 
    Your output should include:
    1. **Content Marketing**: Suggestions for blogs, videos, or other content types. Provide 3-5 actionable steps for implementation.
    2. **Social Media Strategy**: Recommend specific platforms, posting frequency, and campaign ideas, with measurable goals or KPIs.
    3. **Advertising Campaigns**: Outline paid ad strategies (e.g., Google Ads, Facebook Ads). Include budget allocation and expected ROI.
    4. **Search Engine Optimization (SEO)**: Suggest improvements or new tactics, including tools or techniques they can use.
    5. **Innovative Approaches**: Any unique or industry-specific ideas that would differentiate this business.

    For each strategy, explain how it aligns with the business's goals and utilizes its current strengths. Provide a quarterly timeline to help them implement these strategies effectively."""
    
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
    website_url = st.text_input("Enter your business website", placeholder="https://example.com")
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
