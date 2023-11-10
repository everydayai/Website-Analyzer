import streamlit as st
import openai

# Access the OpenAI API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["YOUR_OPENAI_API_KEY"]

st.title("Investment Property Finder in Breckenridge and Blue River, CO")

# User inputs
max_price = st.text_input("Maximum Price")
amenities = st.multiselect("Amenities", ["Close to Skiing", "Hot Tub", "Bus Route", "Parking"])
bedrooms = st.selectbox("Bedrooms", ["1", "2", "3", "4", "5+"])
bathrooms = st.selectbox("Bathrooms", ["1", "2", "3", "4", "5+"])
square_footage = st.selectbox("Square Footage", ["<1000 sqft", "1000-2000 sqft", "2000-3000 sqft", "3000-4000 sqft", "4000+ sqft"])

if st.button('Find Property'):
    # Process the inputs and call the OpenAI API
    user_input = f"You are an AI assistant that provides highly specific investment property recommendations in Breckenridge and 
        Blue River, CO. Consider the user's maximum price, selected amenities, and area preferences to recommend specific neighborhoods 
        or intersections that would be a good fit for investment. Importantly, only recommend areas where short-term rentals are allowed 
        under the new law. I'm considering buying an investment property in Breckenridge and Blue River, CO. My maximum price is {max_price}. I'm 
    looking for these amenities: {', '.join(amenities)}. Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Square Footage: {square_footage}."
    
    # Call the OpenAI API with the chat model
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with the GPT-4 model you are using
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    # Display the response from the API
    st.write(response.choices[0].message['content'])
