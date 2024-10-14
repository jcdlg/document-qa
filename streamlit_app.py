import streamlit as st
from openai import OpenAI


# Show title and description.
#st.markdown("""<span style='color: purple;'>This is a red font color</span>""",unsafe_allow_html=True)
st.logo("png/logo.png", size='large')

st.title('📄 MSL Companion')


# Create an OpenAI client.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a PI:", type=("pdf")
    )
    
    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the PI:",
        placeholder="Provide all indications for NSCLS across all BMS drugs.",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
