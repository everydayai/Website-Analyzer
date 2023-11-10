import streamlit as st
import openai

# Set the OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

st.title("Investment Property Finder in Breckenridge and Blue River, CO")

# User inputs
max_price = st.text_input("Maximum Price")
amenities = st.multiselect("Amenities", ["Close to Skiing", "Hot Tub", "Bus Route", "Parking"])
bedrooms = st.selectbox("Bedrooms", ["1", "2", "3", "4", "5+"])
bathrooms = st.selectbox("Bathrooms", ["1", "2", "3", "4", "5+"])
square_footage = st.selectbox("Square Footage", ["<1000 sqft", "1000-2000 sqft", "2000-3000 sqft", "3000-4000 sqft", "4000+ sqft"])

if st.button('Find Property'):
    # Process the inputs and call the OpenAI API
    user_input = f"I'm considering buying an investment property in Breckenridge and Blue River, CO. My maximum price is {max_price}. I'm looking for these amenities: {', '.join(amenities)}. Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Square Footage: {square_footage}."
    
    # Call the OpenAI API here with the user_input and get the response
    response = openai.Completion.create(
      engine="text-davinci-003", # Replace with your preferred model
      prompt=user_input,
      max_tokens=150
    )

    # Display the response from the API
    st.write(response.choices[0].text.strip())
