import guardrails as gd
import streamlit as st

from src.models import ValidSQL
from src.prompt import PROMPT


@st.cache_resource
def get_guard() -> gd.Guard:
    """
    Create a output guard using GuardRails.
    """
    guard = gd.Guard.from_pydantic(output_class=ValidSQL, prompt=PROMPT)
    return guard
