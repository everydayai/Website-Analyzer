import streamlit as st
import openai

def main():
    st.title("Email Subject Line Generator")

    # Streamlit app setup to use secrets for API key management
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Collect user input about the audience and message
    audience_desc = st.text_input("Describe your audience (e.g., age, interests, profession):", value="", placeholder="e.g., middle-aged professionals interested in sustainability")
    message_content = st.text_area("What is the main message or offer of your email?", value="", placeholder="e.g., Inviting you to join our sustainability webinar")

    # Button to generate email subject lines
    if st.button('Generate Email Subject Lines'):
        subject_lines = generate_subject_lines(audience_desc, message_content)
        if subject_lines:
            st.subheader("Suggested Email Subject Lines and Preheaders:")
            for idx, line in enumerate(subject_lines, 1):
                st.markdown(f"- **{idx}**: {line}")  # Use markdown to format the list
        else:
            st.error("Failed to generate subject lines. Please try again.")

def generate_subject_lines(audience, message):
    try:
        # Correct API call to use GPT-4o for generating subject lines
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Specified to use GPT-4 Omni
            messages=[
                {"role": "system", "content": f"Generate 10 compelling email subject lines and preheaders for an audience that includes {audience}, regarding the following message: {message}"}
            ]
        )
        # Extracting text from the responses
        return [choice['message']['content'] for choice in response.choices]
    except Exception as e:
        st.error(f"An error occurred while generating subject lines: {str(e)}")
        return None

if __name__ == "__main__":
    main()
