import streamlit as st
import openai
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

initial_messages = [{
    "role": "system",
    "content": """
        You are an assistant that helps people plan their first YouTube video. Your suggestions should be geared toward creating engaging content that matches the user's expertise, personality, and interests. Provide a structured plan including:
        - Video Topic
        - Suggested Title
        - Video Outline (main points or segments)
        - Hook/Opening Line
        - Recommended Call to Action
        """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

def CustomChatGPT(user_input, messages):
    query = f"User's expertise and interests: {user_input}. Suggest a structured plan for their first YouTube video."
    messages.append({"role": "user", "content": query})
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Set layout to wide
st.set_page_config(layout="wide")

# Centered title
st.markdown("<h1 style='text-align: center; color: black;'>YouTube Video Planner</h1>", unsafe_allow_html=True)

# Create columns for input and output
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Your Expertise & Interests</h2>", unsafe_allow_html=True)
    user_input = st.text_area("Describe your expertise and interests", placeholder="E.g., cooking, fitness, real estate, technology, travel, etc.")
    generate_button = st.button('Generate Video Plan')

if generate_button:
    messages = initial_messages.copy()
    reply, _ = CustomChatGPT(user_input, messages)

    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Your YouTube Video Plan ⬇️</h2>", unsafe_allow_html=True)
        st.write(reply)

# Contact capture form
st.markdown("<h2 style='text-align: center; color: black;'>Get in Touch for More Help ⬇️</h2>", unsafe_allow_html=True)
with st.form(key='contact_form'):
    name = st.text_input("Your Name", placeholder="Enter your name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    message = st.text_area("Your Message", placeholder="Let us know how we can assist you further")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.success("Thank you for getting in touch! We'll get back to you shortly.")