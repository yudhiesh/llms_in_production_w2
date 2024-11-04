import guardrails as gd
import streamlit as st
from gptcache import Cache
from gptcache.adapter.api import SearchDistanceEvaluation, init_similar_cache
from gptcache.embedding import Onnx
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from gptcache.processor.post import nop
from phoenix.otel import register
from phoenix.trace.openai import OpenAIInstrumentor

from src.models import LLMResponse
from src.prompt import PROMPT


@st.cache_resource
def instrument() -> None:
    """
    Instrument the OpenAI API using Phoenix.
    """

    tracer_provider = register(
        project_name="my-llm-app",
        endpoint="http://localhost:6006/v1/traces",
    )
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)


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
    return gd.Guard.from_pydantic(output_class=LLMResponse, prompt=PROMPT)
