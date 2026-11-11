"""HHD.D Details: copies deadlines, fees and required documents from a UW policy.

Function: extract(policy_text)

Input:
    policy_text (str): the policy text.
    Sample: "The Winter 2027 tuition due date is January 22, 2027. A $20 Change of Registration Fee is charged."

Output (dict):
    deadlines (list of str): dates copied exactly from the policy, such as "January 22, 2027".
    fees (list of str): dollar amounts copied exactly from the policy, such as "$20".
    required_documents (list of str): forms or documents the student must have, such as "I-20".
    Sample: {"deadlines": ["January 22, 2027"], "fees": ["$20"], "required_documents": []}

Every deadline and fee must appear in the policy, word for word.
Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/details.py      Score it: python3 score.py details
"""
import ollama

# This lets the file work both as "python3 llm/details.py" and as "from llm.details import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

KEYS = ["deadlines", "fees", "required_documents"]

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(policy_text):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Policy: {policy_text}
Output:</query>"""
    return prompt


def extract(policy_text):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: every key in KEYS is a list, and every deadline and fee is in policy_text, word for word.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. Return {"deadlines": ..., "fees": ..., "required_documents": ...}.
    raise NotImplementedError("extract is not written yet")


if __name__ == "__main__":
    policy = input("Policy: ")
    print(extract(policy))
