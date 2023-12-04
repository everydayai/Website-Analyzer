import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# Access the OpenAI API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Children's Story and Image Panel Generator")

# User inputs for the story and main character
age_group = st.selectbox("Age Group", ["3-5 years", "6-8 years", "9-12 years"])
theme = st.text_input("Story Theme", placeholder="Enter a theme for the story (e.g., adventure, friendship)")
main_character = st.text_input("Main Character", placeholder="Describe the main character (e.g., a small brave rabbit)")
details = st.text_area("Additional Details", placeholder="Any specific details to include in the story (e.g., a magical forest)")

# Function to generate the story
def generate_story(age_group, theme, main_character, details):
    prompt = f"Write a concise children's story suitable for age group {age_group} about {theme} featuring a main character who is {main_character}. Include details such as {details}. The story should be short enough to fit within 10 panels."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300  # Adjust the token limit as needed
    )
    return response.choices[0].message['content']

# Function to generate images with DALL-E 3
def generate_image(panel_text, main_character):
    try:
        prompt = f"{panel_text}. Visual style: consistent with previous panels. Main character: {main_character}."
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",  # Adjust the size if needed
            model="dall-e-3"  # Specify DALL-E 3 model
        )
        image_url = response['data'][0]['url']
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        return image
    except Exception as e:
        st.error(f"Error in generating image: {e}")
        return None

if st.button('Generate Story and Images'):
    story = generate_story(age_group, theme, main_character, details)
    story_parts = story.split('.')[:10]  # Use the first 10 sentences for panels

    for i, part in enumerate(story_parts):
        if part.strip():  # Ensure part is not empty
            st.subheader(f'Panel {i+1}')
            st.write(part.strip())
            image = generate_image(part, main_character)
            if image:
                st.image(image, caption=f'Image for Panel {i+1}')
