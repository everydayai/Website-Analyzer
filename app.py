import streamlit as st
import openai

def main():
    st.title("Blog Post Idea and Outline Generator")

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    blog_topic = st.text_input("Enter your blog topic:", value="", placeholder="e.g., Artificial Intelligence in Healthcare")
    target_audience = st.text_input("Describe your target audience:", value="", placeholder="e.g., healthcare professionals")
    post_length = st.selectbox("Choose the length of your blog post:", ['Short (500 words)', 'Medium (1000 words)', 'Long (1500+ words)'])

    if st.button('Generate Blog Post Ideas and Outlines'):
        response = generate_blog_ideas_and_outlines(blog_topic, target_audience, post_length)
        if response:
            st.subheader("Suggested Blog Post Ideas and Outlines:")
            st.write(response)
        else:
            st.error("Failed to generate blog post ideas and outlines. Please check the inputs and try again.")

def generate_blog_ideas_and_outlines(topic, audience, length):
    try:
        prompt_text = f"""As an expert content strategist and writer, create 5 unique blog post ideas on the topic of {topic} for {audience}. For each idea, provide a brief outline suitable for a {length} post. Each outline should include:
        1. An attention-grabbing title
        2. 3-5 main sections with brief descriptions
        3. A concluding thought or call-to-action

        Ensure that each idea is distinct and tailored to the interests and needs of the target audience."""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt_text}],
            max_tokens=1000
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    main()