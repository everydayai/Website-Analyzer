import streamlit as st
import openai

# Access the OpenAI API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("AI Lead Magnet Idea Generator for Marketers")

# User inputs for the marketing plan
st.subheader("Tell Us About Your Target Audience")
business_type = st.text_input("Business Type", placeholder="e.g., Real Estate, E-commerce")
target_audience = st.text_area("Target Audience", placeholder="Describe your primary customer base")

# Generate AI lead magnet ideas button
if st.button('Generate AI Lead Magnet Ideas'):
    # Construct the prompt for AI lead magnet ideas
    prompt_text = (
        f"Generate ideas for AI-based lead magnets that a {business_type} company can offer to their target audience: {target_audience}. "
        f"Focus on interactive and engaging AI-driven tools or content that can attract and provide value to their customers."
    )

    # Call the OpenAI API for text generation
    try:
        response_text = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant who specializes in marketing and AI applications."},
                {"role": "user", "content": prompt_text}
            ]
        )
        lead_magnet_ideas = response_text.choices[0].message['content']
    except Exception as e:
        lead_magnet_ideas = f"Error in generating AI lead magnet ideas: {e}"

    # Display the AI lead magnet ideas
    st.markdown("### AI Lead Magnet Ideas")
    st.write(lead_magnet_ideas)

# Rest of your Streamlit code...
