import streamlit as st
import openai
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initial system message setup for the video topic generator
initial_messages = [{
    "role": "system",
    "content": """
    You are an assistant helping a real estate agent brainstorm video topics and outlines. 
    Based on a specified goal or area of focus, suggest five video topics with outlines.
    Each topic should be numbered (1-5) and should include:
    - A catchy title for the video
    - A brief summary of the video's content
    - Key points or segments the video should cover (bullet points)
    """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )

def CustomChatGPT(goal, messages):
    query = f"""
    The real estate agent's goal is: {goal}. 
    Please provide five video topic ideas with the following structure:
    1. Title: A catchy title
    2. Summary: Brief description of the content
    3. Key Points: Bullet points of segments to cover
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
st.markdown("<h1 style='text-align: center; color: black;'>Real Estate Video Topic Generator</h1>", unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h2 style='text-align: center; color: black;'>Your Video Goal</h2>", unsafe_allow_html=True)
    goal = st.text_area("Describe the focus or goal for your videos", placeholder="E.g., attracting first-time homebuyers, showcasing luxury properties, or explaining market trends.")
    generate_button = st.button('Generate Video Topics')

# Process results on button click
if generate_button and goal:
    messages = initial_messages.copy()
    st.session_state["reply"], _ = CustomChatGPT(goal, messages)

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Video Topics & Outlines ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
