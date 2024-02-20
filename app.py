import streamlit as st
import openai

# Access the OpenAI API key from environment variables or secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Plan Your Investment Strategy")

# User inputs
st.subheader("Investment Profile")
age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
investment_experience = st.selectbox("Your Investment Experience", ["Beginner", "Intermediate", "Advanced"])
investment_goal = st.text_input("Investment Goal", placeholder="e.g., Retirement, Buying a Home, Education")

st.subheader("Financial Information")
annual_income = st.number_input("Annual Income", min_value=10000, max_value=1000000, step=1000)  # Removed format argument
investment_amount = st.number_input("Amount Available for Investment", min_value=1000, max_value=500000, step=100)  # Removed format argument
risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])

if st.button('Generate My Investment Strategy'):
    # Construct the prompt for the AI
    prompt_text = (
        f"Generate an investment strategy for a {age}-year-old with {investment_experience} experience. "
        f"Investment goal: {investment_goal}. Annual income: {annual_income}. "
        f"Amount available for investment: {investment_amount}. Risk tolerance: {risk_tolerance}."
    )

    # Call the OpenAI API for text generation
    try:
        response_text = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI specializing in personalized investment strategies."},
                {"role": "user", "content": prompt_text}
            ]
        )
        investment_strategy = response_text.choices[0].message['content']
    except Exception as e:
        investment_strategy = f"Error in generating investment strategy: {e}"

    # Display the investment strategy
    st.markdown("### Your Personalized Investment Strategy")
    st.write(investment_strategy)

# Disclaimer
st.write("Disclaimer: This tool provides suggestions based on AI-generated content. Please ensure to conduct your own research or consult with a financial advisor before making any investment decisions.")
