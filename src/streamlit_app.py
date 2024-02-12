import time

import guardrails as gd
import openai
import streamlit as st

from src.cached_resources import get_guard
from src.constants import OPENAI_MODEL_ARGUMENTS
from src.models import ValidSQL
from src.utils import get_openai_api_key

st.set_page_config(page_title="SQL Code Generator")
st.title("SQL Code Generator")


def generate_response(input_text: str, guard: gd.Guard) -> None:
    """
    Generate a response for the given input text taking in the cache and guard.
    """
    try:
        start_time = time.time()

        (_, validated_response, _, validation_passed, error,) = guard(
            openai.chat.completions.create,
            prompt_params={
                "nl_instruction": input_text,
            },
            **OPENAI_MODEL_ARGUMENTS,
        )
        total_time = time.time() - start_time
        if error or not validation_passed or not validated_response:
            st.error(f"Unable to produce an answer due to: {error}")
        else:
            valid_sql = ValidSQL(**validated_response)
            generated_sql = valid_sql.generated_sql
            st.info(generated_sql)
            st.info(f"That query took: {total_time:.2f}s")

    except Exception as e:
        st.error(f"Error: {e}")


def main() -> None:
    guard = get_guard()
    get_openai_api_key()
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            generate_response(text, guard)


if __name__ == "__main__":
    main()
