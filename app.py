import streamlit as st
import openai

def main():
    st.title("Email Subject Line Generator")

    # Streamlit app setup to use secrets for API key management
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Collect user input about the audience, message, and desired tone
    audience_desc = st.text_input("Describe your audience (e.g., age, interests, profession):", value="", placeholder="e.g., middle-aged professionals interested in sustainability")
    message_content = st.text_area("What is the main message or offer of your email?", value="", placeholder="e.g., Inviting you to join our sustainability webinar")
    tone = st.selectbox("Choose the tone for your email subject lines:", ['Friendly', 'Professional', 'Urgent', 'Curious', 'Humorous', 'Informative'])

    # Button to generate email subject lines
    if st.button('Generate Email Subject Lines'):
        subject_lines = generate_subject_lines(audience_desc, message_content, tone)
        if subject_lines:
            st.subheader("Suggested Email Subject Lines and Preheaders:")
            for idx, line in enumerate(subject_lines, 1):
                st.markdown(f"- **{idx}**: {line}")
        else:
            st.error("Failed to generate subject lines. Please try again.")

def generate_subject_lines(audience, message, tone):
    try:
        # API call to generate subject lines, specifying tone and focusing on quality
        prompt_text = f"Create 10 high-quality email subject lines under 7 words each, tailored for an audience that includes {audience}. The tone should be {tone.lower()}, focusing on the message: {message}. Ensure these subject lines are optimized for high open rates."
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Using GPT-4 Omni
            messages=[
                {"role": "system", "content": prompt_text}
            ]
        )
        # Extracting and filtering text from the responses
        subject_lines = [choice['message']['content'] for choice in response.choices]
        # Ensure each subject line is under 7 words
        return [line for line in subject_lines if len(line.split()) <= 7]
    except Exception as e:
        st.error(f"An error occurred while generating subject lines: {str(e)}")
        return None

if __name__ == "__main__":
    main()
