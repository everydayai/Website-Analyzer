import streamlit as st
import openai

# Initializing Streamlit app
st.title("AI Integration Assessment for Businesses")

# Securely accessing the OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to call OpenAI API using GPT-4o
def call_openai_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Specify GPT-4o as the model
            messages=[
                {"role": "system", "content": prompt['system']},
                {"role": "user", "content": prompt['user']}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Streamlit UI for input
business_type = st.text_input("Describe your business type and main activities:", "e.g., Manufacturing")
current_tech_usage = st.text_input("Describe current technology usage in your business:", "e.g., Mostly manual processes with some Excel usage")
ai_interest_areas = st.multiselect("Select potential areas for AI integration:", 
                                   ["Customer Service", "Operations", "Marketing", "Risk Management", "Product Development"])

generate_button = st.button('Generate AI Integration Report')

# Handling the button click
if generate_button:
    user_prompt = {
        "system": """
        You are an AI consultant tasked with evaluating a business to determine where AI can be effectively integrated. Provide a detailed report that assesses the current technology usage and recommends areas for AI implementation based on the business type and interests.""",
        "user": f"""
        Business Type: {business_type}
        Current Technology Usage: {current_tech_usage}
        Interest Areas: {', '.join(ai_interest_areas)}"""
    }
    report = call_openai_api(user_prompt)
    if report:
        st.markdown("### AI Integration Report")
        st.write(report)
    else:
        st.write("An error occurred while generating the report. Please try again.")
