import os
import time

import guardrails as gd
import openai
import streamlit as st
from gptcache import Cache
from gptcache.adapter.api import SearchDistanceEvaluation, get, init_similar_cache, put
from gptcache.embedding import Onnx
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from gptcache.processor.post import nop

from src.constants import OPENAI_MODEL_ARGUMENTS, PROMPT
from src.models import ValidSQL

st.set_page_config(page_title="SQL Code Generator")
st.title("SQL Code Generator")


def get_openai_api_key() -> None:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    os.environ["OPENAI_API_KEY"] = openai_api_key
    if not openai_api_key.startswith("sk-"):
        st.error("Please enter your OpenAI API key!", icon="⚠️")


@st.cache_resource
def get_cache() -> Cache:
    inner_cache = Cache()
    onnx = Onnx()
    data_manager = get_data_manager(
        CacheBase("sqlite"),
        VectorBase("faiss", dimension=onnx.dimension),
    )
    init_similar_cache(
        cache_obj=inner_cache,
        post_func=nop,
        data_manager=data_manager,
        evaluation=SearchDistanceEvaluation(),
    )
    return inner_cache


@st.cache_resource
def get_guard() -> gd.Guard:
    guard = gd.Guard.from_pydantic(output_class=ValidSQL, prompt=PROMPT)
    return guard


def generate_response(input_text: str, cache: Cache, guard: gd.Guard) -> None:
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
                put(input_text, generated_sql, cache_obj=cache)

        else:
            total_time = time.time() - start_time
            st.info(cached_result[0])
            st.info(f"That query took: {total_time:.2f}s")
    except Exception as e:
        st.error(f"Error: {e}")


def main() -> None:
    guard = get_guard()
    cache = get_cache()
    get_openai_api_key()
    with st.form("my_form"):
        st.warning("Our models can make mistakes!", icon="🚨")
        text = st.text_area(
            "Enter text:",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            generate_response(text, cache, guard)


if __name__ == "__main__":
    main()
