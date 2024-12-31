import streamlit as st
import pyperclip
from post_generator import generate_post, post_to_linkedin
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Kannada"]

# Main app layout
def main():
    st.subheader("LinkedIn Post Generator with Images")

    # User input for custom prompt
    custom_prompt = st.text_area("Enter your topic or idea for the post:", placeholder="E.g., Share your insights on AI trends.")

    # Dropdown for Length and Language
    col1, col2 = st.columns(2)

    with col1:
        selected_length = st.selectbox("Length", options=length_options)

    with col2:
        selected_language = st.selectbox("Language", options=language_options)

    # File uploader for images
    uploaded_files = st.file_uploader("Upload images for your post (optional)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Initialize the generated_post variable in session state
    if "generated_post" not in st.session_state:
        st.session_state.generated_post = ""

    # Generate Button
    if st.button("Generate"):
        if custom_prompt.strip():
            st.session_state.generated_post = generate_post(custom_prompt, selected_length, selected_language)
        else:
            st.warning("Please enter a topic or idea for the post.")

    # Display the generated post if it exists
    if st.session_state.generated_post:
        st.text_area("Generated Content", st.session_state.generated_post, height=500)

        # Copy Button
        if st.button("Copy"):
            pyperclip.copy(st.session_state.generated_post)
            st.success("Text copied successfully!")

        # Post on LinkedIn Button
        if st.button("Post on LinkedIn"):
            with st.spinner("Posting to LinkedIn..."):
                try:
                    response = post_to_linkedin(st.session_state.generated_post, uploaded_files)
                    st.success("Post created successfully on LinkedIn!")
                except Exception as e:
                    st.error(f"Failed to post on LinkedIn: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()
