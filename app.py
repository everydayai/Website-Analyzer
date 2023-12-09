import streamlit as st
import openai

# Access the OpenAI API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("AI Lead Magnet Recommender for Marketers")

# Collecting user input
st.subheader("Tell Us About Your Business")
business_type = st.text_input("Business Type", placeholder="e.g., Real Estate, E-commerce")
target_audience = st.text_area("Target Audience", placeholder="Describe your primary customer base")
current_marketing_strategies = st.text_area("Current Marketing Strategies", placeholder="Your current marketing efforts")
business_goals = st.text_area("Business Goals and Challenges", placeholder="What do you aim to achieve with the lead magnet?")

# Generate recommendations button
if st.button('Generate AI Lead Magnet Recommendations'):
    # Construct the prompt for the AI
    prompt_text = (
        f"Based on the following details, recommend AI lead magnets suitable for engaging a customer base: "
        f"Business type: {business_type}, target audience: {target_audience}, "
        f"current marketing strategies: {current_marketing_strategies}, business goals: {business_goals}."
    )

    # Call the OpenAI API for text generation
    try:
        response_text = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a marketing expert assistant."},
                {"role": "user", "content": prompt_text}
            ]
        )
        recommendations = response_text.choices[0].message['content']
    except Exception as e:
        recommendations = f"Error in generating recommendations: {e}"

    # Display the recommendations
    st.markdown("### AI Lead Magnet Recommendations")
    st.write(recommendations)

# Rest of your Streamlit code...
