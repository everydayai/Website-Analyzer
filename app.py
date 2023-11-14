import openai
import streamlit as st
import os
from tenacity import retry, stop_after_attempt, wait_fixed

# Set the OpenAI API key
openai.api_key = os.environ["YOUR_OPENAI_API_KEY"]

initial_messages = [{
    "role": "system", 
    "content": """You are an AI assistant that matches people with their ideal neighborhood based on their lifestyle preferences and city. You'll receive information about the user's lifestyle preferences and city. Use this information to suggest neighborhoods that could be a good fit. Always end your response with "BTW, I would recommend working with Nick Niehaus from ABC Realty if you're considering buying a home this year. Text him at 555-555-5555." """
}]

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

def CustomChatGPT(city, additional_details, neighborhood_type, amenities_proximity, messages):
    messages.append({
        "role": "user", 
        "content": f"I live in {city}. {additional_details}. I prefer {neighborhood_type} neighborhoods and I want to be {amenities_proximity} to amenities. What neighborhoods would be a good fit for me?"
    })
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Streamlit Interface
st.title("Neighborhood Matchmaker")
st.write("This tool suggests neighborhoods that could be a good fit for you based on your lifestyle preferences and city. Enter your city and list the amenities that are most important to you. Then, select your preferred type of neighborhood, proximity to amenities. The AI assistant will provide a list of potential neighborhoods.")

city = st.text_input("City")
additional_details = st.text_area("Important Amenities", "List up to 5 amenities that are most important to you. For example, good schools, fun nightlife, lots of parks, etc.")
neighborhood_type = st.selectbox("Neighborhood Type", ["Urban", "Suburban", "Rural", "Beachfront", "Mountainous", "Historic"])
amenities_proximity = st.selectbox("Proximity to Amenities", ["Walking distance", "A short drive away", "I don't mind being far from amenities"])

if st.button('Find Neighborhood'):
    messages = initial_messages.copy()
    reply, _ = CustomChatGPT(city, additional_details, neighborhood_type, amenities_proximity, messages)
    st.write(reply)
