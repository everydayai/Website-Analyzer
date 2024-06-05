import streamlit as st
import openai

def main():
    st.title("Email Subject Line Generator")

    # Collect user input about the audience and message
    audience_desc = st.text_input("Describe your audience (e.g., age, interests, profession):", "e.g., middle-aged professionals interested in sustainability")
    message_content = st.text_area("What is the main message or offer of your email?", "e.g., Inviting you to join our sustainability webinar")

    # Button to generate email subject lines
    if st.button('Generate Email Subject Lines'):
        subject_lines = generate_subject_lines(audience_desc, message_content)
        if subject_lines:
            st.subheader("Suggested Email Subject Lines and Preheaders:")
            for idx, line in enumerate(subject_lines, 1):
                st.text(f"{idx}. {line}")
        else:
            st.error("Failed to generate subject lines. Please try again.")

def generate_subject_lines(audience, message):
    try:
        # OpenAI API call to generate subject lines
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Generate 10 compelling email subject lines and preheaders for an audience that includes {audience}, regarding the following message: {message}",
            max_tokens=150,
            n=10,
            stop=None,
            temperature=0.7
        )
        # Extracting text from the responses
        return [choice['text'].strip() for choice in response.choices]
    except Exception as e:
        st.error(f"An error occurred while generating subject lines: {str(e)}")
        return None

if __name__ == "__main__":
    main()
