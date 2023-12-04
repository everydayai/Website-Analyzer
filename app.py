import streamlit as st
import openai
import os

# Access the OpenAI API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("2024 Lead Generation Plan Creator for Small Businesses")

# User inputs for creating the lead generation plan
st.subheader("Tell Us About Your Business")
business_description = st.text_area("Business Description", placeholder="Describe your business (e.g., nature, services/products, size).")
target_customers = st.text_area("Target Customers", placeholder="Describe your ideal customers (e.g., demographics, interests, locations).")
advertising_budget = st.selectbox("Advertising Budget", ["No budget", "Limited budget", "Moderate budget", "Large budget"])
additional_details = st.text_area("Additional Details", placeholder="Any specific goals or strategies you've considered?")

# Function to generate the lead generation plan
def generate_lead_generation_plan(business_description, target_customers, advertising_budget, additional_details):
    prompt = f"Create a detailed lead generation plan for 2024 for a business described as follows: {business_description}. The target customers are: {target_customers}. The advertising budget is: {advertising_budget}. Additional details: {additional_details}. Include step-by-step instructions and strategies for implementing lead generation systems."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a marketing expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500  # Adjust the token limit as needed
    )
    return response.choices[0].message['content']

if st.button('Generate Lead Generation Plan'):
    plan = generate_lead_generation_plan(business_description, target_customers, advertising_budget, additional_details)
    st.subheader("Your Customized Lead Generation Plan for 2024:")
    st.write(plan)
