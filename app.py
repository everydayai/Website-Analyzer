import streamlit as st
import openai
import os
import urllib.parse

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

initial_messages = [{
    "role": "system",
    "content": """
        You are a neighborhood matchmaker. Given a person's preferences in terms of amenities, lifestyle, and priorities, suggest three neighborhoods that best match their needs in a specified city. For each neighborhood, include the full location in the format: Neighborhood, City, State, and keep descriptions concise (one or two sentences).
    """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300  # Limit tokens to keep responses concise
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

# Initialize session state for storing the API reply
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
    st.session_state["reply"], _ = CustomChatGPT(city, preferences, messages)  # Store response in session state

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Recommended Neighborhoods ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
        
        # Extract only lines with the format "Neighborhood, City, State:"
        neighborhoods = []
        for line in st.session_state["reply"].splitlines():
            if line and "," in line and ":" in line:  # Ensure it matches "Neighborhood, City, State:"
                location = line.split(":")[0].strip()  # Capture up to the first colon
                # Remove any numbering
                if location[0].isdigit():
                    location = location.split(" ", 1)[1].strip()
                neighborhoods.append(location)
        
        # Display Zillow links
        st.markdown("### Zillow Search Links")
        for location in neighborhoods:
            # Format the search query correctly
            full_location_query = urllib.parse.quote(location)
            zillow_url = f"https://www.zillow.com/homes/{full_location_query}_rb/"
            
            st.markdown(f"- [Search for homes in {location} on Zillow]({zillow_url})")
