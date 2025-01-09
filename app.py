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

def generate_marketing_plan(content, goals, budget, location_focus, campaign_focus, location, inferred_info, messages, fallback=False):
    """
    Generates a marketing plan based on provided content, goals, budget, and optional focuses.
    """
    location_info = f"The business is located in {location}." if location else "No specific location was mentioned."
    additional_info = f"Inferred details: {inferred_info}" if inferred_info else "No additional business details were inferred."
    location_focus_info = "Focus on location-specific strategies." if location_focus else "No explicit focus on location-specific strategies."
    campaign_focus_info = f"Specific focus: {campaign_focus}" if campaign_focus else "No specific campaign focus provided."

    query = f"""
    The user has provided the following details:
    - Content: {content if not fallback else "N/A (no content provided)"}
    - Goals for 2025: {goals}
    - Marketing budget for 2025: ${budget}
    - {location_info}
    - {location_focus_info}
    - {campaign_focus_info}
    - {additional_info}

    Create a detailed 1-year marketing plan that includes:
    1. **Overview Summary**: Summarize the key focus areas for the business to achieve its goals. Include video marketing as a top priority.
    2. **Advanced Keywords**: Provide at least 10 long-tail keywords specific to the industry and location (if applicable).
    3. **Content Topics**: Provide at least 10 blog, YouTube, or social media topics, each with a brief description.
    4. **SEO Strategies**: Detailed recommendations for improving search rankings, including tools and methods.
    5. **Content Marketing Plan**: How to leverage the provided content topics to achieve the stated goals.
    6. **Social Media Strategies**: Platforms, posting frequency, campaign ideas, and location-specific tactics.
    7. **Advertising Campaigns**: Platforms, budget allocation, target audience details, and creative strategies.
    8. **Execution Timeline**: A quarterly breakdown of actionable steps with measurable KPIs.

    Ensure the recommendations are detailed, actionable, and tailored to the business's specific goals, budget, and location.
    Avoid generic suggestions and provide unique, high-value insights.
    """
    
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
    - Unique strategies tailored to the business's goals, location, and target audience.
    - Innovative advertising campaigns and emerging platform recommendations.
    - Video marketing as a critical strategy across all platforms.
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
st.markdown("<h2 style='text-align: center; color: black;'>Enter Business Details</h2>", unsafe_allow_html=True)
website_url = st.text_input("Enter your business website (optional)", placeholder="e.g., https://example.com")
manual_details = st.text_area(
    "Enter details about your business (if no website is provided or cannot be scanned)", 
    placeholder="E.g., Business name, target audience, goals, and location."
)
goals = st.text_area("Goals for 2025 (optional)", placeholder="E.g., increase brand awareness, drive online sales")
budget = st.number_input("Marketing Budget for 2025 ($)", min_value=1000, step=1000)

# Additional inputs for focus areas
location_focus = st.checkbox("Focus on location-specific strategies?")
campaign_focus = st.text_input(
    "Specific campaign focus (optional)", 
    placeholder="E.g., lead generation, email campaigns, brand awareness"
)

generate_button = st.button('Generate Marketing Plan')

# Process results on button click
if generate_button:
    st.session_state["show_notice"] = True
    with st.spinner("Analyzing provided details and preparing your report..."):
        # Attempt to scrape website content if a URL is provided
        website_content, scrape_successful = scrape_website(website_url) if website_url else ("", False)
        location = extract_location(website_content) if scrape_successful else None
        inferred_info = infer_business_info_from_url(website_url) if not scrape_successful and website_url else None

        # Use manual details as fallback content
        content = website_content if scrape_successful else manual_details
        fallback_mode = not scrape_successful and not manual_details

        if fallback_mode:
            st.warning("No valid website content or manual details provided. Please enter business details.")

        messages = initial_messages.copy()
        st.session_state["reply"] = generate_marketing_plan(
            content, goals, budget, location_focus, campaign_focus, location, inferred_info, messages, fallback=fallback_mode
        )
        st.session_state["show_notice"] = False  # Remove the notice once the report is ready

# Display the waiting notice
if st.session_state["show_notice"]:
    st.info("Generating your marketing plan. This process may take a minute or two. Please wait...")

# Display results if there is a reply in session state
if st.session_state["reply"]:
    st.markdown("<h2 style='text-align: center; color: black;'>Your 2025 Marketing Plan ⬇️</h2>", unsafe_allow_html=True)
    st.markdown(st.session_state["reply"])
