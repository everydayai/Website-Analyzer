import streamlit as st
import openai
import os

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initial system message setup for the emoji adder
initial_messages = [{
    "role": "system",
    "content": """
    You are an assistant that adds appropriate emojis to a given text. 
    Analyze the content for tone, context, and meaning, and then insert emojis 
    in a way that enhances the message without overwhelming it. 
    The style of emoji usage will depend on the user's preferences for tone, density, and placement.
    """
}]

def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500  # Adjust based on the expected length of emoji-enhanced output
    )

def CustomChatGPT(text, tone, density, placement, messages):
    query = f"""
    Enhance the following text by adding emojis based on these preferences:
    - Tone: {tone}
    - Density: {density}
    - Placement: {placement}
    
    Text: {text}
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
st.markdown("<h1 style='text-align: center; color: black;'>Emoji Enhancer Tool</h1>", unsafe_allow_html=True)

# User inputs
st.markdown("<h2 style='text-align: center; color: black;'>Customize Your Emojis</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    user_text = st.text_area("Paste your text here", placeholder="Enter your text...")

    # Dropdown menus for user customization
    tone = st.selectbox(
        "Select the tone:",
        ["Friendly", "Professional", "Playful", "Romantic", "Excited"]
    )
    density = st.selectbox(
        "Select emoji density:",
        ["Minimal (few emojis)", "Moderate (balanced emojis)", "Heavy (lots of emojis)"]
    )
    placement = st.selectbox(
        "Select emoji placement:",
        ["At the end of sentences", "Inline with text", "Start of key points"]
    )

    add_emojis_button = st.button('Add Emojis')

# Process results on button click
if add_emojis_button and user_text:
    messages = initial_messages.copy()
    st.session_state["reply"], _ = CustomChatGPT(user_text, tone, density, placement, messages)

# Display results if there is a reply in session state
if st.session_state["reply"]:
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Enhanced Text ⬇️</h2>", unsafe_allow_html=True)
        st.write(st.session_state["reply"])
