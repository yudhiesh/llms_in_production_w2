import guardrails as gd
import streamlit as st
from redisvl.extensions.llmcache import SemanticCache
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
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
def get_cache() -> SemanticCache:
    """
    Create a cache using RedisVL SemanticCache.
    """
    llmcache = SemanticCache(
        name="llmcache",                    
        prefix="llmcache",                   
        redis_url="redis://redis:6379",      
        distance_threshold=0.1               
    )
    return llmcache

@st.cache_resource
def get_guard() -> gd.Guard:
    """
    Create an output guard using GuardRails.
    """
    return gd.Guard.from_pydantic(output_class=LLMResponse, prompt=PROMPT)
