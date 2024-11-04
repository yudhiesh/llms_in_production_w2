import os

import streamlit as st


def get_openai_api_key() -> None:
    """
    Get the OpenAI API key from the user.
    """
    key = os.environ["OPENAI_API_KEY"]
    if not key.startswith("sk-"):
        st.error("Please enter your OpenAI API key!", icon="⚠️")
