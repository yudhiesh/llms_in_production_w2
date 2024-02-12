import os

import streamlit as st


def get_openai_api_key() -> None:
    """
    Get the OpenAI API key from the user.
    """
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    os.environ["OPENAI_API_KEY"] = openai_api_key
    if not openai_api_key.startswith("sk-"):
        st.error("Please enter your OpenAI API key!", icon="⚠️")
