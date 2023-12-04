import streamlit as st
import openai
import os

# Access the OpenAI API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Comprehensive Lead Generation Plan for 2024")

# User inputs for creating the lead generation plan
st.subheader("Describe Your Business")
business_description = st.text_area(
    "Business Description",
    placeholder="Briefly describe your business, including products/services offered."
)

st.subheader("Target Audience")
target_customers = st.text_area(
    "Target Customers",
    placeholder="Describe your ideal customers (e.g., demographics, interests)."
)

st.subheader("Budget and Preferences")
advertising_budget = st.selectbox(
    "Advertising Budget",
    ["No budget", "Limited budget", "Moderate budget", "Large budget"]
)
additional_details = st.text_area(
    "Additional Details",
    placeholder="Any specific goals, strategies, or preferences?"
)

# Function to generate the lead generation plan
def generate_lead_generation_plan(business_description, target_customers, advertising_budget, additional_details):
    prompt = (
        f"Create a detailed lead generation plan for 2024 for a business with the following details: "
        f"Description: {business_description}; Target customers: {target_customers}; "
        f"Advertising budget: {advertising_budget}. Additional details: {additional_details}. "
        "Include specific ad placements, creative opt-in strategies, video marketing ideas, and AI lead generation tools."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a marketing expert providing detailed lead generation plans."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700
    )
    return response.choices[0].message['content']

# Generate and display the plan
if st.button('Generate Lead Generation Plan'):
    plan = generate_lead_generation_plan(
        business_description, target_customers, advertising_budget, additional_details
    )
    st.subheader("Your Customized Lead Generation Plan for 2024:")
    st.write(plan)
