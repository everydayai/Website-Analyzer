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
        prompt_text = f"""You are an expert level copywriter who specializes in writing email subject lines and preheaders that get opened at
        extremely high rates. First, you will consider a range of 100 possible ideas based on the input you'll receive from me. You will then 
        analyze these ideas from the perspective of the ideal customer who receives the email. You will select from your ideas the ones that 
        are most likely to get clicked and opened. Each of the ideas you share should be unique in a way that would allow them to stand out
        in an email inbox. Generate 100 pairs of compelling email subject lines and preheaders for {audience}, message: {message}, tone: {tone}. 
        Each subject line should be under 7 words, and each preheader should complement the subject line. Reply with a list of the best 10 combinations."""
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
