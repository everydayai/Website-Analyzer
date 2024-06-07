import streamlit as st
import openai

def main():
    st.title("Email Subject Line and Preheader Generator")
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    audience_desc = st.text_input("Describe your audience:", value="", placeholder="e.g., middle-aged professionals")
    message_content = st.text_area("Main message or offer of your email:", value="", placeholder="e.g., Join our webinar")
    tone = st.selectbox("Choose the tone for your email subject lines:", ['Friendly', 'Professional', 'Urgent', 'Curious'])

    if st.button('Generate Email Subject Lines and Preheaders'):
        subject_lines, preheaders = generate_subject_lines_and_preheaders(audience_desc, message_content, tone)
        if subject_lines:
            st.subheader("Suggested Email Subject Lines and Preheaders:")
            for idx, (line, preheader) in enumerate(zip(subject_lines, preheaders), 1):
                st.markdown(f"- **Subject Line {idx}**: {line}")
                st.markdown(f"  - **Preheader {idx}**: {preheader}")
        else:
            st.error("Failed to generate subject lines and preheaders. Please check the inputs and try again.")

def generate_subject_lines_and_preheaders(audience, message, tone):
    try:
        prompt_text = f"""...Your existing prompt..."""
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt_text}],
            max_tokens=500
        )
        # Debug print to check response structure
        print("Debug: Full API Response:", response)  
        # Extracting subject lines and preheaders using newline split
        pairs = response.choices[0].message['content'].split('\n\n')[1:]  # Skipping the first line which is usually an introductory line
        subject_lines = [pair.split('\n')[0] for pair in pairs]
        preheaders = [pair.split('\n')[1] for pair in pairs]
        return subject_lines, preheaders
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None

if __name__ == "__main__":
    main()