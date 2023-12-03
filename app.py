import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# Access the OpenAI API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["YOUR_OPENAI_API_KEY"]

st.title("Children's Story and Image Panel Generator")

# User inputs for the story
age_group = st.selectbox("Age Group", ["3-5 years", "6-8 years", "9-12 years"])
theme = st.text_input("Story Theme", placeholder="Enter a theme for the story (e.g., adventure, friendship)")
details = st.text_area("Additional Details", placeholder="Any specific details to include in the story (e.g., a brave rabbit, a magical forest)")

# Function to generate the story
def generate_story(age_group, theme, details):
    prompt = f"Write a children's story for age group {age_group} about {theme}. Include details such as {details}."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative writer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

# Function to generate images
def generate_image(panel_text):
    try:
        response = openai.Image.create(
            prompt=panel_text,
            n=1,
            size="1024x1024"  # Adjust the size if needed
        )
        image_url = response['data'][0]['url']
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        return image
    except Exception as e:
        return None

if st.button('Generate Story and Images'):
    story = generate_story(age_group, theme, details)
    story_parts = story.split('.')[:10]  # Generate images for first 10 parts

    for i, part in enumerate(story_parts):
        st.subheader(f'Panel {i+1}')
        st.write(part.strip())
        image = generate_image(part)
        if image:
            st.image(image, caption=f'Image for Panel {i+1}')
        else:
            st.error("Error in generating image for this part of the story.")
