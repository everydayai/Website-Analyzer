import streamlit as st
import openai

# Access the OpenAI API key from Hugging Face Spaces secrets or your environment variables
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Video Script Generator")

# Define video styles and their descriptions
video_styles = {
    "Explainer": "Explainer videos break down complex concepts into simple, engaging visuals and narratives.",
    "Testimonial": "Testimonial videos feature satisfied customers sharing their positive experiences.",
    "Product Demo": "Product demos showcase the features and benefits of a product in action.",
    "How-To": "How-to videos provide step-by-step instructions on performing a task or using a product.",
    "Brand Story": "Brand story videos share the company's mission, vision, and values, connecting emotionally with the audience."
}

# User selects the video style
video_style = st.selectbox("Choose the style of video you want to create:", options=list(video_styles.keys()))

# Display the description of the selected video style
st.write(f"**Description:** {video_styles[video_style]}")

# Additional inputs
business_name = st.text_input("Business Name", "Your Business Name")
target_audience = st.text_area("Target Audience", "Describe your target audience.")

# Button to generate video script
if st.button('Generate Video Script'):
    # Construct the prompt for the AI
    prompt_text = f"Create a script for a {video_style.lower()} video for '{business_name}' targeting '{target_audience}'. {video_styles[video_style]}"
    
    # Call the OpenAI API for text generation
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_text,
            max_tokens=500,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        script = response.choices[0].text.strip()
    except Exception as e:
        script = f"Error in generating script: {e}"
    
    # Display the generated script
    st.markdown("### Generated Video Script")
    st.write(script)

# Disclaimer
st.write("Disclaimer: This tool provides AI-generated suggestions. Please review and customize the script to fit your specific business needs.")
