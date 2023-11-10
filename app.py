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
    user_input = (
        """You are an AI assistant that provides highly specific investment property recommendations in Breckenridge and 
        Blue River, CO. Consider the user's maximum price, selected amenities, and area preferences to recommend specific neighborhoods 
        or intersections that would be a good fit for investment. Importantly, only recommend areas where short-term rentals are allowed 
        under the new law. I'm considering buying an investment property in Breckenridge and Blue River, CO. My maximum price is {max_price}. I'm
        looking for these amenities: {', '.join(amenities)}. Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Square Footage: {square_footage}.
        Only reply with neighborhoods from this list of approved neighborhoods:
Boulder Ridge Sub
Peak 8 Place
Glenwild sub
Twin Elk Lodge
Saw Mill Patch Townhomes
Sawmill Creek Village
Breckenridge Park Meadows Condo
 Wildwood Lodge Condo
 Sunset Condo
Double Eagle Condo
Four O’Clock Condo
Tyra Summit Condo #3 Mountaineer
Wedgewood Condo
Retreat Condo
Winterpoint Townhomes
Antlers Lodge Condominiums
Skyway Lodge Condo
Jenni Exchange Condo
Snider Addition
Bartlett & Shock Sub
Journal Building Condo
Ski Hill Condo
Georgia Square Condo
River Mountain Lodge Condo
Sawmill Creek Condo
Sawmill Creek Village Sub
Pine Ridge Condo
Blazing Saddles Condo
Main Street Mall Condo
Park Place Condo
Sundowner II Condos
Sundowner Condo
Cimarron Condo
One Breckenridge Place
Columbine Condo
Winterpoint Townhomes
Trails End Condo
Cedars At Breckenridge Townhomes
Der Steiermark Condo
Mountainwood Condo
Park Avenue Lofts Condo
Snodallion Condo
Timbernest Condo
Powderhorn Condo
Pine Creek Townhomes
Tannenbaum By The River
Mother Lode Condo
Base 9 Condo
Snowdrop Condo
Lance’s West Condo
Miners Candle Condo
Lift Condo
Snowspruce Condo
Inner Circle Condo
Christiana Condo
Tamarisk Condo
Village Point Townhomes At Breck
Corral At Breckenridge
Snowflake
Chimney Ridge Townhomes
Highlander Townhomes
Elk Ridge Townhomes
Kings Ridge Condo
Los Pinos 
Westridge Townhomes
Westridge Cluster Homes
Tyra IV Riverbend Lodge Condo
Saddlewood condo
Timber Trail Sub
Tyra Summit Condo                                                                   
Crystal Peak Lodge
One Ski Hill Place					
Mountain Thunder Lodge
River Mountain Lodge Condo
Main Street Junction 
Main Street Station Condo
Water House on Main Breck
Village At Breckenridge
Plaza Three Condo AKA Wetterhorn
Liftside Condo
Chateaux Condominium Hotel
Marriot Mountain Valley Lodge AKA Hotel Breckenridge
Beaver Run Condo
Bluesky Breckenridge Condo

96 Subdivision
97 South Subdivision
97 Subdivision
Aspen View
Blue Rock Springs
Bryce Estates
Clyde Lode
Coronet
Crown
Blue River Condos 
Golden Crown
Lakeshore
Leap Year
Louise Placer
McCullough Gulch
Mountain View
New Eldorado
New Eldorado Townhomes
Pennsylvania Canyon
Rivershore
Royal
Sherwood Forest
Silverheels
Smith Mining Claim
Spillway
Sunny Slope
Timber Creek Estates 
Timber Line
Wilderness
"""
    )
    
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
