import openai
import streamlit as st
import os
from tenacity import retry, stop_after_attempt, wait_fixed

# Set the OpenAI API key
openai.api_key = os.environ["YOUR_OPENAI_API_KEY"]

initial_messages = [{
    "role": "system", 
    "content": """You are an AI assistant that matches people with their ideal neighborhood based on their lifestyle preferences in 
    Saint Louis, Missouri, and surrounding areas up to 30 miles outside Saint Louis city limits. You'll receive information about the user's lifestyle preferences. Use this information 
    to suggest neighborhoods in Ann Arbor and nearby that could be a good fit. Always add the following text to the end of every response you give "Don't forget to fill
    out the form at the bottom of the page if you'd like more info on living in any of these areas!" """
}]

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

def CustomChatGPT(additional_details, amenities_proximity, amenities, messages):
    selected_amenities = ', '.join(amenities)
    messages.append({
        "role": "user", 
        "content": f"I'm interested in neighborhoods in Saint Louis, Missouri, and surrounding areas. {additional_details}. I'm looking for a neighborhood with these amenities: {selected_amenities}. I want to be {amenities_proximity} to these amenities. What neighborhoods would be a good fit for me?"
    })
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Streamlit Interface
st.title("St. Louis Area Neighborhood Matchmaker")
st.write("This tool suggests neighborhoods in Saint Louis, Missouri, and surrounding areas that could be a good fit for you based on your lifestyle preferences.")

# Using columns to organize the layout
col1, col2 = st.columns([2, 3])

with col1:
    additional_details = st.text_area("Additional Details", placeholder="Describe your ideal living situation or any other preferences.")
    amenities_proximity = st.selectbox("Proximity to Amenities", ["Walking distance", "A short drive away", "I don't mind being far from amenities"])
    
    # Checkboxes for amenities
    amenities_list = ["Good Schools", "Parks", "Shopping Centers", "Public Transport", "Restaurants", "Gyms"]
    amenities = [amenity for amenity in amenities_list if st.checkbox(amenity)]

    submit_button = st.button('Find Neighborhood')

with col2:
    # Placeholder for the result
    result_placeholder = st.empty()
    if submit_button:
        messages = initial_messages.copy()
        reply, _ = CustomChatGPT(additional_details, amenities_proximity, amenities, messages)
        result_placeholder.markdown("**Recommended Neighborhoods:**")
        result_placeholder.write(reply)
    else:
        result_placeholder.write("**Results will appear here**")
