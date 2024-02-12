import guardrails as gd
import streamlit as st
from gptcache import Cache
from gptcache.adapter.api import SearchDistanceEvaluation, init_similar_cache
from gptcache.embedding import Onnx
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from gptcache.processor.post import nop
from phoenix.trace.openai import OpenAIInstrumentor

from src.constants import PROMPT
from src.models import ValidSQL


@st.cache_resource
def instrument() -> None:
    """
    Instrument the OpenAI API using Phoenix.
    """
    OpenAIInstrumentor().instrument()


@st.cache_resource
def get_cache() -> Cache:
    """
    Create a cache using GPTCache.
    """
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
    """
    Create a output guard using GuardRails.
    """
    guard = gd.Guard.from_pydantic(output_class=ValidSQL, prompt=PROMPT)
    return guard
