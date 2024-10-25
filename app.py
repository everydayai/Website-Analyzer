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
        max_tokens=300
    )

def parse_neighborhoods(response_text):
    """
    Parse the response text to extract neighborhood information.
    Returns a list of dictionaries containing neighborhood info.
    """
    neighborhoods = []
    lines = response_text.strip().split('\n')
    current_entry = None
    
    for line in lines:
        line = line.strip()
        if line and (line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
            if ':' in line:
                location_parts = line.split(':', 1)[0].split(',')
                if len(location_parts) >= 3:
                    neighborhood = location_parts[0].split('.', 1)[1].strip()
                    city = location_parts[1].strip()
                    state = location_parts[2].strip()
                    neighborhoods.append({
                        'neighborhood': neighborhood,
                        'city': city,
                        'state': state,
                        'full': f"{neighborhood}, {city}, {state}"
                    })
    
    return neighborhoods

def format_zillow_search(neighborhood_info):
    """
    Format the location string for Zillow search.
    Uses Zillow's homes search format with the neighborhood name in the query.
    """
    # Clean and format the search terms
    clean_neighborhood = neighborhood_info['neighborhood'].replace('&', 'and')
    clean_city = neighborhood_info['city']
    clean_state = neighborhood_info['state']
    
    # Create the search query
    search_query = f"{clean_neighborhood} {clean_city} {clean_state}"
    encoded_query = urllib.parse.quote(search_query)
    
    # Use Zillow's current search URL format
    return f"https://www.zillow.com/homes/{encoded_query}_rb/"

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
        
        if neighborhoods:
            st.markdown("### 🏠 Zillow Search Links")
            for hood in neighborhoods:
                zillow_url = format_zillow_search(hood)
                st.markdown(f"- [Search homes in {hood['neighborhood']}]({zillow_url})")
        else:
            st.warning("Unable to generate Zillow links. Please try again.")