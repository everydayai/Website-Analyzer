import streamlit as st
import openai

def main():
    st.title("Engagement Ring Selector")
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    fiancée_description = st.text_input("Describe your fiancée:", value="", placeholder="e.g., loves classic style, has a vibrant personality")
    relationship_details = st.text_area("Details about your relationship:", value="", placeholder="e.g., together for 3 years, love hiking and traveling")
    budget = st.selectbox("Select your budget range:", ['Under $1,000', '$1,000 - $3,000', '$3,000 - $5,000', 'Above $5,000'])

    if st.button('Generate Ring Suggestions'):
        response = generate_ring_suggestions(fiancée_description, relationship_details, budget)
        if response:
            st.subheader("Suggested Engagement Rings:")
            st.write(response)
        else:
            st.error("Failed to generate ring suggestions. Please check the inputs and try again.")

def generate_ring_suggestions(fiancée_description, relationship_details, budget):
    try:
        prompt_text = f"""You are a world-class jewelry expert specializing in engagement rings. Based on the following information, provide 10 unique 
        engagement ring suggestions that would perfectly suit the described fiancée and their relationship. Consider the style preferences, personality, 
        and budget while making your suggestions. Include details about the ring's design, gemstone, metal, and any special features.
        
        Fiancée Description: {fiancée_description}
        Relationship Details: {relationship_details}
        Budget: {budget}
        
        Reply with a list of the best 10 engagement ring options."""
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
