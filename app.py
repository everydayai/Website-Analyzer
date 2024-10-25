import streamlit as st
import openai
import os
import urllib.parse

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

initial_messages = [{
    "role": "system",
    "content": """
        You are a neighborhood matchmaker. Given a person's preferences in terms of amenities, lifestyle, and priorities, suggest three neighborhoods that best match their needs in a specified city. For each neighborhood, include the full location in the format: Neighborhood, City, State, and provide a short description highlighting its unique qualities.
    """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

def CustomChatGPT(city, preferences, messages):
    query = f"User is looking for neighborhoods in {city} with these preferences: {preferences}. Suggest suitable neighborhoods and describe each briefly, including the full location as Neighborhood, City, State."
    messages.append({"role": "user", "content": query})
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Streamlit setup
st.set_page_config(layout="wide")

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
    reply, _ = CustomChatGPT(city, preferences, messages)
    
    # Display the results
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Recommended Neighborhoods ⬇️</h2>", unsafe_allow_html=True)
        st.write(reply)
        
        # Extract neighborhood, city, and state information
        neighborhoods = []
        for line in reply.splitlines():
            if ":" in line:
                location = line.split(":")[0].strip()  # Full location "Neighborhood, City, State"
                # Remove any leading numbering
                if location[0].isdigit():
                    location = location.split(" ", 1)[1].strip()
                neighborhoods.append(location)
        
        # Display Zillow links, focusing on city and state first, then adding neighborhood if needed
        st.markdown("### Zillow Search Links")
        for location in neighborhoods:
            # Simplify the search query to prevent Zillow from returning specific listings
            city_state_query = urllib.parse.quote(f"{city}, {location.split(',')[-1].strip()}")
            zillow_url = f"https://www.zillow.com/homes/{city_state_query}_rb/"
            
            # Add neighborhood to query if broader city/state search isn't suitable
            if city.lower() not in location.lower():
                location_query = urllib.parse.quote(location)
                zillow_url = f"https://www.zillow.com/homes/{location_query}_rb/"
            
            st.markdown(f"- [Search for homes in {location} on Zillow]({zillow_url})")
