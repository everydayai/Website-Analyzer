import streamlit as st
import openai

# Access the OpenAI API key from environment variables or secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Personalized 6-Month Fitness and Health Plan Generator")

# User inputs
st.subheader("About You")
name = st.text_input("Your Name", placeholder="Enter your name")
age = st.number_input("Your Age", min_value=12, max_value=100, step=1)
gender = st.selectbox("Your Gender", ["Female", "Male", "Prefer not to say"])

st.subheader("Current Fitness and Health Status")
current_fitness_level = st.selectbox("Your Current Fitness Level", ["Beginner", "Intermediate", "Advanced"])
current_health_issues = st.text_area("Current Health Issues", placeholder="Any known health issues or concerns")
dietary_preferences = st.text_area("Dietary Preferences", placeholder="e.g., Vegan, Gluten-free, Keto, No preferences")

st.subheader("Your Fitness Goals")
fitness_goals = st.multiselect("Select Your Fitness Goals", ["Weight loss", "Muscle gain", "Endurance improvement", "Flexibility", "General well-being"])
goal_timeframe = st.selectbox("Goal Timeframe", ["3 months", "6 months", "1 year"])

if st.button('Generate My Fitness Plan'):
    # Construct the prompt for the AI
    prompt_text = (
        f"Create a personalized 6-month fitness and health plan for {name}, a {age}-year-old {gender} with {current_fitness_level} fitness level. "
        f"Health issues: {current_health_issues}. Dietary preferences: {dietary_preferences}. Fitness goals: {', '.join(fitness_goals)} over {goal_timeframe}."
    )

    # Call the OpenAI API for text generation
    try:
        response_text = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI fitness coach."},
                {"role": "user", "content": prompt_text}
            ]
        )
        fitness_plan = response_text.choices[0].message['content']
    except Exception as e:
        fitness_plan = f"Error in generating fitness plan: {e}"

    # Display the fitness plan
    st.markdown("### Your Personalized 6-Month Fitness Plan")
    st.write(fitness_plan)

# Disclaimer
st.write("Disclaimer: This tool provides suggestions based on AI-generated content. Please consult with a healthcare provider or a professional fitness trainer before starting any new fitness program.")
