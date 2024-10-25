import streamlit as st
import openai
import os
import urllib.parse

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

initial_messages = [{
    "role": "system",
    "content": """
    You are a neighborhood matchmaker. Given a person's preferences in terms of amenities, 
    lifestyle, and priorities, suggest exactly three neighborhoods that best match their needs 
    in a specified city. For each neighborhood, start with a numbered line (1., 2., or 3.) 
    followed by the full location in the format: 'Neighborhood, City, State:' then provide 
    a brief description on the next line.
    """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300  # Limit tokens to keep responses concise
    )

def parse_neighborhoods(response_text):
    """
    Parse the response text to extract neighborhood information more reliably.
    Returns a list of tuples containing (neighborhood name, full location string)
    """
    neighborhoods = []
    current_location = ""
    
    # Split the response into lines and process each line
    lines = response_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        # Look for lines that start with a number and contain location info
        if line and (line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
            if ':' in line:
                # Remove the number and leading space
                location = line.split('.', 1)[1].strip()
                # Split at the colon to get just the location part
                location = location.split(':', 1)[0].strip()
                if ',' in location:
                    neighborhoods.append(location)
    
    return neighborhoods

def format_zillow_search(location):
    """
    Format the location string for Zillow search, handling special characters and spaces.
    """
    # Remove any special characters and extra spaces
    clean_location = ' '.join(location.split())
    # Encode the location for URL
    encoded_location = urllib.parse.quote(clean_location)
    # Create the Zillow search URL
    return f"https://www.zillow.com/homes/{encoded_location}_rb/"

def CustomChatGPT(city, preferences, messages):
    query = f"""
    User is looking for neighborhoods in {city} with these preferences: {preferences}. 
    Please suggest exactly 3 suitable neighborhoods. For each one:
    1. Start with a number (1., 2., or 3.)
    2. Provide the full location as 'Neighborhood, City, State:'
    3. Add a brief description on the next line
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
st.markdown("<h1 style='text-align: center; color: black;'>Ideal Neighborhood Finder</h1>", unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Your Preferences</h2>", unsafe_allow_html=True)
    city = st.text_input("City", placeholder="Enter the city you want to search in")
    preferences = st.text_area("Describe your ideal neighborhood", placeholder="E.g., family-friendly, near parks, vibrant nightlife")
    generate_button = st.button('Find Neighborhoods')

# Process results on button click
if generate_button and city and preferences:
    messages = initial_messages.copy()
    st.session_state["reply"], _ = CustomChatGPT(city, preferences, messages)

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Recommended Neighborhoods ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
        
        # Extract and display Zillow links
        neighborhoods = parse_neighborhoods(st.session_state["reply"])
        
        if neighborhoods:  # Only show the section if we successfully parsed neighborhoods
            st.markdown("### 🏠 Zillow Search Links")
            for location in neighborhoods:
                zillow_url = format_zillow_search(location)
                st.markdown(f"- [Search homes in {location}]({zillow_url})")
        else:
            st.warning("Unable to generate Zillow links. Please try again.")