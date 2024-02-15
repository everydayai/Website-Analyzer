import streamlit as st
import openai

# Access the OpenAI API key from environment variables or secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Find Your Ideal Neighborhood")

# User inputs
st.subheader("About You")
age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
occupation = st.text_input("Your Occupation", placeholder="e.g., Software Developer, Teacher")

st.subheader("Lifestyle and Preferences")
preferred_climate = st.selectbox("Preferred Climate", ["Warm", "Temperate", "Cold"])
interests = st.text_area("Interests", placeholder="e.g., Outdoor activities, Arts and culture, Nightlife")
housing_budget = st.number_input("Housing Budget", min_value=500, max_value=10000, step=100, format="$%i")

st.subheader("Your Ideal Neighborhood")
neighborhood_preferences = st.multiselect("Select Your Neighborhood Preferences", ["Safe", "Family-friendly", "Vibrant nightlife", "Quiet", "Pet-friendly", "Close to nature", "Urban"])
commute_preference = st.selectbox("Preferred Commute Time", ["Less than 15 minutes", "15-30 minutes", "30-60 minutes", "More than an hour"])

if st.button('Find My Ideal Neighborhood'):
    # Construct the prompt for the AI
    prompt_text = (
        f"Find an ideal neighborhood for the user, a {age}-year-old working as {occupation}. "
        f"Preferred climate: {preferred_climate}. Interests: {interests}. Housing budget: {housing_budget}. "
        f"Neighborhood preferences: {', '.join(neighborhood_preferences)} with a preferred commute time of {commute_preference}."
    )

    # Call the OpenAI API for text generation
    try:
        response_text = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI specializing in neighborhood recommendations."},
                {"role": "user", "content": prompt_text}
            ]
        )
        neighborhood_recommendation = response_text.choices[0].message['content']
    except Exception as e:
        neighborhood_recommendation = f"Error in finding ideal neighborhood: {e}"

    # Display the neighborhood recommendation
    st.markdown("### Your Ideal Neighborhood Recommendation")
    st.write(neighborhood_recommendation)

# Disclaimer
st.write("Disclaimer: This tool provides suggestions based on AI-generated content. Please ensure to conduct your own research or consult with a real estate professional before making any decisions.")
