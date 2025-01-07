import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re

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
            continue

    return " ".join(all_content[:3000]), scrape_successful

def infer_business_info_from_url(url):
    """
    Infer business details from the domain name.
    """
    domain_name = urlparse(url).netloc
    inferred_info = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a business analyst. Based on domain names, generate likely information about a business, including its industry, target audience, and goals."
            },
            {
                "role": "user",
                "content": f"The domain is {domain_name}. What can you infer about this business?"
            }
        ]
    )
    return inferred_info["choices"][0]["message"]["content"]

def extract_location(content):
    """
    Extract a possible location from the website content using regular expressions.
    """
    location_match = re.search(r'\b(?:serving|located in|offices in|based in)\s([\w\s,]+)', content, re.IGNORECASE)
    return location_match.group(1).strip() if location_match else None

def generate_marketing_plan(website_content, industry, goals, budget, location, inferred_info, messages, fallback=False):
    """
    Generates a marketing plan based on website content, industry, goals, and budget.
    """
    location_info = f"The business is located in {location}." if location else "No specific location was mentioned."
    additional_info = f"Inferred details: {inferred_info}" if inferred_info else "No additional business details were inferred."

    query = f"""
    The user has provided the following details:
    - Website content: {website_content if not fallback else "N/A (website content could not be retrieved)"}
    - Industry: {industry}
    - Goals for 2025: {goals}
    - Marketing budget for 2025: ${budget}
    - {location_info}
    - {additional_info}

    Create a detailed 1-year marketing plan that includes:
    1. **Advanced Keywords**: Long-tail keywords specific to the industry and location (if applicable).
    2. **Content Topics**: Blog and YouTube video topics that target the business's goals and location.
    3. **Social Media Strategies**: Platform recommendations, post frequency, and campaign ideas tailored to the location.
    4. **Advertising Campaigns**: Target audience, platforms, and budget breakdowns, integrating location-specific targeting.
    5. **Emerging Platforms**: Recommendations for new or underutilized platforms.
    6. **SEO Improvements**: Tools, techniques, and steps to improve search rankings.
    7. **Execution Plan**: Actionable, step-by-step instructions for implementation with quarterly timelines.
    Ensure all suggestions align with the business's strengths, and avoid generic or obvious recommendations."""
    
    messages.append({"role": "user", "content": query})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response["choices"][0]["message"]["content"]

# Define initial_messages
initial_messages = [{
    "role": "system",
    "content": """You are a world-class marketing strategist trained by Neil Patel, David Ogilvy, and Seth Godin. 
    Your task is to create highly customized marketing plans based on user input. Incorporate any business location 
    or target areas explicitly mentioned in the website content or user-provided details into the recommendations.
    Go beyond generic suggestions, and include:
    - Specific, long-tail keywords to target.
    - Detailed content ideas, including blogs, videos, and social media campaigns.
    - Unique strategies tailored to the business's industry, goals, and location.
    - Innovative advertising campaigns and emerging platform recommendations.
    Ensure every suggestion is actionable and includes measurable KPIs."""
}]

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
    industry = st.text_input("Industry (optional)", placeholder="E.g., Real Estate, Retail, Technology")
    goals = st.text_area("Goals for 2025 (optional)", placeholder="E.g., increase brand awareness, drive online sales")
    budget = st.number_input("Marketing Budget for 2025 ($)", min_value=1000, step=1000)
    generate_button = st.button('Generate Marketing Plan')

# Process results on button click
if generate_button:
    st.session_state["show_notice"] = True
    with st.spinner("Analyzing website content and preparing your report..."):
        website_content, scrape_successful = scrape_website(website_url) if website_url else ("", False)
        location = extract_location(website_content) if scrape_successful else None
        inferred_info = infer_business_info_from_url(website_url) if not scrape_successful else None
    fallback_mode = not scrape_successful
    if fallback_mode:
        st.warning("Unable to retrieve website content. Generating recommendations based on inferred details.")
    messages = initial_messages.copy()
    st.session_state["reply"] = generate_marketing_plan(
        website_content if scrape_successful else "N/A", 
        industry, goals, budget, location, inferred_info, messages, fallback=fallback_mode
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
