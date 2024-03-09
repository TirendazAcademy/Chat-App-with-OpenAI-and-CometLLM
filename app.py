import comet_llm
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv(override=True)

comet_llm.init(
    project="Blog-Title-Generator",
    workspace = "tirendaz-academy",
    api_key = os.environ["COMET_ML_API"])

def get_response(user_content):   
    start = time.time()  
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a world-class blogger who loves to write engaging titles for a keyword. Generate 10 attention-grabbing blog titles based on user-provided keywords."},
            {"role": "user", "content": user_content},
        ],
        max_tokens=1024,
    )
    duration = time.time() - start

    comet_llm.log_prompt(
        prompt=user_content,
        output=response.choices[0].message.content,
        duration=duration * 1000,
    )

    return response.choices[0].message.content

st.title("Blog Title Generator")
user_content = st.text_input("Enter the keyword for blog titles:")
if st.button("Generate Titles"):
    if not user_content:
        st.warning('Please enter a keyword before generating titles.', icon="⚠️")
    generated_titles = get_response(user_content)
    st.success("Titles generated successfully!")
    st.text_area("", value=generated_titles, height=300)