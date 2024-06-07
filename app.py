import streamlit as st
import openai

def main():
    st.title("Email Subject Line and Preheader Generator")
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    audience_desc = st.text_input("Describe your audience:", value="", placeholder="e.g., middle-aged professionals")
    message_content = st.text_area("Main message or offer of your email:", value="", placeholder="e.g., Join our webinar")
    tone = st.selectbox("Choose the tone for your email subject lines:", ['Friendly', 'Professional', 'Urgent', 'Curious'])

    if st.button('Generate Email Subject Lines and Preheaders'):
        response = generate_subject_lines_and_preheaders(audience_desc, message_content, tone)
        if response:
            st.subheader("Suggested Email Subject Lines and Preheaders:")
            st.write(response)  # Directly display the response
        else:
            st.error("Failed to generate subject lines and preheaders. Please check the inputs and try again.")

def generate_subject_lines_and_preheaders(audience, message, tone):
    try:
        prompt_text = f"""Generate 10 pairs of compelling email subject lines and preheaders for an audience interested in {audience} about '{message}', in a {tone.lower()} tone. Each subject line should be under 7 words, and each preheader should complement the subject line. Display them as a list."""
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt_text}],
            max_tokens=500
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    main()
