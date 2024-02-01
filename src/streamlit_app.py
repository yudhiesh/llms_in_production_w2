import os
import time

import guardrails as gd
import openai
import streamlit as st
from gptcache import Cache, Config
from gptcache.adapter.api import get, init_similar_cache, put
from gptcache.processor.post import nop
from gptcache.processor.pre import get_prompt

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


@st.cache_resource
def get_cache():
    cache.init(pre_embedding_func=get_prompt)
    inner_cache = Cache()
    init_similar_cache(
        cache_obj=inner_cache, post_func=nop, config=Config(similarity_threshold=0.9)
    )
    return inner_cache


@st.cache_resource
def get_guard():
    guard = gd.Guard.from_pydantic(output_class=ValidSQL, prompt=PROMPT)
    return guard


guard = get_guard()
cache = get_cache()


def generate_response(input_text: str, cache: Cache) -> None:
    try:
        start_time = time.time()
        cached_result = get(input_text, cache_obj=cache, top_k=1)
        if not cached_result:
            (
                raw_llm_response,
                validated_response,
                reask,
                validation_passed,
                error,
            ) = guard(
                openai.chat.completions.create,
                prompt_params={"nl_instruction": input_text},
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
                put(input_text, generated_sql, cache_obj=cache)

        else:
            total_time = time.time() - start_time
            st.info(cached_result[0])
            st.info(f"That query took: {total_time:.2f}s")
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
        generate_response(text, cache)
