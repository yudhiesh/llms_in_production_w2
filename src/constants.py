PROMPT = """

Generate a valid SQL query for the following natural language instruction:

${nl_instruction}

${gr.complete_json_suffix}
"""
MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 2048
TEMPERATURE = 0.0

OPENAI_MODEL_ARGUMENTS = dict(
    model=MODEL_NAME,
    max_tokens=MAX_TOKENS,
    temperature=TEMPERATURE,
)
