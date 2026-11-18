import streamlit as st
from openai import OpenAI


st.title("Terminator Translator")

languages = [
    "Portuguese",
    "Japanese",
    "English",
    "Korean",
    "Hindi",
    "French",
    "Chinese",
]

api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("Add OPENAI_API_KEY to the app's Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

with st.form("translator_form"):
    input_language = st.selectbox("Translate from", languages)
    output_language = st.selectbox("Translate to", languages)
    message = st.text_area("Enter text to translate")
    submitted = st.form_submit_button("Translate")

if submitted:
    if not message.strip():
        st.warning("Please enter text to translate.")
    else:
        system_message = (
            "You are a translator. Translate the user's message from "
            f"{input_language} to {output_language}. "
            "Return only the translation."
        )

        with st.spinner("Translating..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message},
                ],
            )

        st.write(response.choices[0].message.content)
