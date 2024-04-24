import streamlit as st
import openai

# Initializing Streamlit app
st.title("Video Script Generator for Small Businesses")

# Accessing the OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to call OpenAI API
def call_openai_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": prompt['system']
                },
                {"role": "user", "content": prompt['user']}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Streamlit UI for input
business_description = st.text_area("Describe your business or video topic/idea:", placeholder="e.g., We are a local bakery specializing in gluten-free pastries.")
problem_solved = st.text_input("What problem do you solve for your customers?", placeholder="e.g., Making gluten-free living delicious and easy.")
services_offered = st.text_input("What services do you want to mention in your video?", placeholder="e.g., Custom gluten-free cakes for special occasions.")
unique_aspects = st.text_input("What makes you unique or separates you from others in your industry?", placeholder="e.g., Our secret family recipes.")
name_to_include = st.text_input("List any names (your name or business name) you want to include in the video.", placeholder="e.g., 123 Custom Blinds or Mary Smith")
call_to_action = st.text_input("How do you want to be contacted? (Provide one call to action)", placeholder="e.g., Visit our bakery on Main Street.")
script_length = st.number_input("Desired script length (maximum word count):", min_value=50, max_value=250, value=150, step=10)

generate_button = st.button('Generate Video Script')

# Handling button click
if generate_button:
    # Creating the prompt as a dictionary
    user_prompt = {
        "system": """
        Act as a small business marketing video script writer. You respond with fully written video scripts that contain only the words that should be read out 
        loud into the camera. The scripts you create do not include shot directions, references to who is speaking, or any other extraneous notes that are not the actual 
        words that should be read out loud. As a small business video marketing expert, you have studied the most effective marketing and social media videos made by small 
        businesses. The video scripts are short, always coming in under the specified maximum word count. They always begin with engaging opening lines that tease what the 
        rest of the video is about and they end with a single strong call to action.""",
        "user": f"""
        Industry: {business_description}
        Problem Solved: {problem_solved}
        Services Offered: {services_offered}
        Unique Aspects: {unique_aspects}
        Names to Include: {name_to_include}
        Call to Action: {call_to_action}
        Script Length: {script_length} words maximum."""
    }
    script = call_openai_api(user_prompt)
    if script:
        st.markdown("### Generated Video Script")
        st.write(script)
    else:
        st.write("An error occurred while generating the script. Please try again.")
