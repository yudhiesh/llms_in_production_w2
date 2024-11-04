PROMPT = """
Generate a valid SQL query for the following natural language instruction:

Query: ${query}

${gr.complete_json_suffix_v3}
"""
