import streamlit as st
import openai

def main():
    st.title("Email Subject Line Generator")
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    audience_desc = st.text_input("Describe your audience:", value="", placeholder="e.g., middle-aged professionals")
    message_content = st.text_area("Main message or offer of your email:", value="", placeholder="e.g., Join our webinar")
    tone = st.selectbox("Choose the tone for your email subject lines:", ['Friendly', 'Professional', 'Urgent', 'Curious'])

    if st.button('Generate Email Subject Lines'):
        subject_lines = generate_subject_lines(audience_desc, message_content, tone)
        if subject_lines:
            st.subheader("Suggested Email Subject Lines and Preheaders:")
            for idx, line in enumerate(subject_lines, 1):
                st.markdown(f"- **{idx}**: {line}")
        else:
            st.error("Failed to generate subject lines. Please check the inputs and try again.")

def generate_subject_lines(audience, message, tone):
    try:
        prompt_text = f"Generate 10 compelling email subject lines for {audience}, message: {message}, tone: {tone}."
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt_text}]
        )
        return [choice['message']['content'] for choice in response.choices]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    main()
