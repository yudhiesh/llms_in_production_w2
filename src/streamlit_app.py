import os

import guardrails as gd
import openai
import streamlit as st

from src.constants import OPENAI_MODEL_ARGUMENTS, PROMPT
from src.models import ValidSQL

# TODO:
# FOR W2
# 3. Setup Semantic Caching
# 4. Setup Arize Phoenix using OpenAI

# FOR W1
# 1. Remove use of LangChain
# 2. Use Rail Str instead of Pydantic due to support issues

st.set_page_config(page_title="SQL Code Generator")
st.title("SQL Code Generator")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
os.environ["OPENAI_API_KEY"] = openai_api_key

guard = gd.Guard.from_pydantic(output_class=ValidSQL, prompt=PROMPT)


def generate_response(input_text: str) -> None:
    try:
        raw_llm_response, validated_response, reask, validation_passed, error = guard(
            openai.chat.completions.create,
            prompt_params={"nl_instruction": input_text},
            **OPENAI_MODEL_ARGUMENTS,
        )
        if error or not validation_passed or not validated_response:
            st.error(f"Unable to produce an answer due to: {error}")
        else:
            valid_sql = ValidSQL(**validated_response)
            generated_sql = valid_sql.generated_sql
            st.info(generated_sql)
    except Exception as e:
        st.error(f"Error: {e}")


with st.form("my_form"):
    st.warning("Our models can make mistakes!", icon="🚨")
    text = st.text_area(
        "Enter text:",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.error("Please enter your OpenAI API key!", icon="⚠️")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)
