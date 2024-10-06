import streamlit as st
import openai
import os
import folium
from streamlit_folium import st_folium
import urllib.parse
import subprocess

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

# Ensure folium is installed
try:
    import folium
except ModuleNotFoundError:
    subprocess.check_call(["python", "-m", "pip", "install", "folium"])
    import folium

initial_messages = [{
    "role": "system",
    "content": """
        You are a neighborhood matchmaker. Given a person's preferences in terms of amenities, lifestyle, and priorities, suggest three neighborhoods that best match their needs. Provide a short description for each neighborhood, including key features such as nearby amenities, atmosphere, and suitability for the user's preferences.
        """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

def CustomChatGPT(preferences, messages):
    query = f"User preferences: {preferences}. Suggest suitable neighborhoods."
    messages.append({"role": "user", "content": query})
    response = call_openai_api(messages)
    ChatGPT_reply = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Set layout to wide
st.set_page_config(layout="wide")

# Initialize session state for storing the results
if "reply" not in st.session_state:
    st.session_state.reply = ""

# Centered title
st.markdown("<h1 style='text-align: center; color: black;'>Neighborhood Matchmaker</h1>", unsafe_allow_html=True)

# Create columns for input and output
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Your Preferences</h2>", unsafe_allow_html=True)
    preferences = st.text_area("Describe your ideal neighborhood", placeholder="E.g., family-friendly, good schools, near parks, vibrant nightlife, public transportation, etc.")
    generate_button = st.button('Find Neighborhoods')

if generate_button:
    messages = initial_messages.copy()
    reply, _ = CustomChatGPT(preferences, messages)
    st.session_state.reply = reply  # Store the reply in session state

if st.session_state.reply:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Recommended Neighborhoods ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state.reply)

        # Add map integration
        st.markdown("<h2 style='text-align: center; color: black;'>Map of Suggested Neighborhoods ⬇️</h2>", unsafe_allow_html=True)
        map_center = [37.7749, -122.4194]  # Default to San Francisco coordinates
        m = folium.Map(location=map_center, zoom_start=12)

        # Placeholder coordinates for neighborhoods (these should be updated with actual data)
        neighborhoods = [
            {"name": "Neighborhood 1", "coordinates": [37.7749, -122.4194]},
            {"name": "Neighborhood 2", "coordinates": [37.7849, -122.4094]},
            {"name": "Neighborhood 3", "coordinates": [37.7649, -122.4294]}
        ]

        for neighborhood in neighborhoods:
            folium.Marker(
                location=neighborhood["coordinates"],
                popup=neighborhood["name"],
                icon=folium.Icon(color='blue')
            ).add_to(m)

        st_folium(m, width=700, height=500)

        # Add Zillow search links for neighborhoods
        st.markdown("<h2 style='text-align: center; color: black;'>Search for Homes in Suggested Neighborhoods ⬇️</h2>", unsafe_allow_html=True)
        for neighborhood in neighborhoods:
            query = urllib.parse.quote(neighborhood["name"])
            zillow_url = f"https://www.zillow.com/homes/{query}_rb/"
            st.markdown(f"[Search for homes in {neighborhood['name']} on Zillow]({zillow_url})")

# Contact capture form
st.markdown("<h2 style='text-align: center; color: black;'>Get in Touch for More Details ⬇️</h2>", unsafe_allow_html=True)
with st.form(key='contact_form'):
    name = st.text_input("Your Name", placeholder="Enter your name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    message = st.text_area("Your Message", placeholder="Let us know how we can assist you further")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.success("Thank you for getting in touch! We'll get back to you shortly.")