import streamlit as st
from openai import OpenAI
import context_utils

# Show title and description.
st.logo("png/logo.png", size="large")
st.title("📄 MSL Companion")
st.subheader(
    "A case study on how to use LLMs to empower MSL teams at Bristol Myers Squibb."
)

# Example queries:

# INDICATIONS BY TA
# List all the indications that you know about, and list them by drug name.
# I am a medical science liaison visiting a pulmonologist.  List all indications that he would care about.
# Which questions are most relevant for OPDIVO for a pulmonologist.

# COMBINATIONS
# Can yervoy be combined with Opdivo?
# For which indications can Yervoy and Opdivo be combined?

# Additional input:
# Efficacy data
# Side effects
# Contraindications

# Create an OpenAI client.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    question = st.text_area(
        "Ask a question about the PI:",
        placeholder="Provide all indications for NSCLS across all BMS drugs.",
    )

    if question:
        prompt = """Answer the following question only using the provided context and if the answer is not contained within the context, say "I am sorry, I don't know."
                    Be as thorough and complete as possible.  Include the drug name as a reference."""
        context = context_utils.get_context()
        messages = [
            {
                "role": "system",
                "content": prompt
                + f"  \n\n---\n\n  Context: {context} \n\n---\n\n Question: {question}",
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
