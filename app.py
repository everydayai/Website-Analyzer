import streamlit as st
import openai
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

initial_messages = [{
    "role": "system",
    "content": """
    You are a painting cost estimator. Given details about a home (square footage, 
    number of stories, type of painting: interior, exterior, or both), provide an estimated 
    cost for painting the home. Include a brief explanation of how the estimate is calculated, 
    and break down the cost if possible.
    """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )

def CustomChatGPT(home_size, stories, paint_type, messages):
    query = f"""
    User has a home with the following specifications:
    - Square footage: {home_size} sqft
    - Number of stories: {stories}
    - Painting type requested: {paint_type}
    
    Please provide an estimated cost to paint the home. Include a breakdown if possible.
    """
    
    messages.append({"role": "user", "content": query})
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Streamlit setup
st.set_page_config(layout="wide")

# Initialize session state
if "reply" not in st.session_state:
    st.session_state["reply"] = None

# Centered title
st.markdown("<h1 style='text-align: center; color: black;'>Home Painting Cost Estimator</h1>", unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Enter Home Details</h2>", unsafe_allow_html=True)
    home_size = st.number_input("Square Footage of Home", min_value=100, max_value=10000, step=50)
    stories = st.selectbox("Number of Stories", options=["1", "2", "3"])
    paint_type = st.selectbox("Type of Painting", options=["Interior", "Exterior", "Both"])
    generate_button = st.button('Estimate Painting Cost')

# Process results on button click
if generate_button and home_size > 0:
    messages = initial_messages.copy()
    st.session_state["reply"], _ = CustomChatGPT(home_size, stories, paint_type, messages)

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Estimated Painting Cost ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
