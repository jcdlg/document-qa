import streamlit as st
from openai import OpenAI
import json
import context_utils

# Show title and description.
st.logo("png/logo.png", size="large")
st.title("📄 MSL Companion")
st.subheader("A case study on how to use LLMs to empower MSL teams at Bristol Myers Squibb.")

# Create an OpenAI client.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    question = st.text_area(
        "Ask a question about the indications in the PI:",
        placeholder="Provide all indications you know aobut for NSCLC.",
    )

    if question:
        prompt = """You are an expert in medical affairs at a pharmaceutical company.  You are an expert in drugs that work with receptors, including agonists, antagonists, inverse agonists, or membrane transport inhibitors.  You are an expert in identifying treatments by line of therapy.  

        Answer the following question ONLY using the content provided below and if the question cannot be answered using the content provided only, say "I am not sure, keep in mind I am only aware of BMS products".  Be thorough and complete.  If you are asked to list indications, include the drug name for each.   
        
        After each paragraph, provide the sources used from the context in the format "Source:".

        """
        context = context_utils.get_context()
        messages = [
            {
                "role": "system",
                "content": prompt
                + f"  \n\n---\n\n  Context: {context} \n\n---\n\n",
            },
            {
                "role": "user",
                "content": f"Question: {question}",
            }
        ]

        # Debug print
       # json_object = json.loads([messages])
        print(json.dumps(messages, indent = 2).replace('\\n','\n'))
        
        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
