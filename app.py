import streamlit as st
import openai
import urllib.parse

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = 'your_openai_api_key'

# Function to get neighborhood suggestions from OpenAI
def suggest_neighborhoods(user_preferences, city=""):
    prompt = (f"Based on the following preferences, suggest neighborhoods in {city}: {user_preferences}. "
              "For each neighborhood, provide a brief description including its main attractions and why it would suit these preferences.")
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to generate Zillow search link for a neighborhood
def generate_zillow_link(neighborhood):
    neighborhood_query = urllib.parse.quote(neighborhood)
    return f"https://www.zillow.com/homes/{neighborhood_query}_rb/"

# Streamlit Interface
st.title("Ideal Neighborhood Finder")
st.write("Describe what you're looking for in an ideal neighborhood, and we'll suggest neighborhoods with Zillow links for homes in those areas.")

# User Inputs
city = st.text_input("City", placeholder="Enter the city you want to search in")
user_preferences = st.text_area("Describe Your Ideal Neighborhood", placeholder="E.g., close to schools, parks, public transit, vibrant nightlife, etc.")

if st.button("Find Neighborhoods"):
    if city and user_preferences:
        # Get neighborhood suggestions from OpenAI
        neighborhoods = suggest_neighborhoods(user_preferences, city)
        
        # Display results
        st.subheader("Neighborhood Suggestions")
        for neighborhood in neighborhoods.splitlines():
            if neighborhood:  # Filter out empty lines
                zillow_link = generate_zillow_link(neighborhood)
                st.markdown(f"- **{neighborhood}**: [View homes on Zillow]({zillow_link})")
    else:
        st.error("Please provide both a city and a description of your ideal neighborhood.")
