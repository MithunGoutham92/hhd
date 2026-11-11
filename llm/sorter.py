"""HHD.A Sorter: decides which UW office should answer a student's question, and how urgent it is.

Function: classify(message)

Input:
    message (str): the question in English, with personal details hidden.
    Sample: "How do I get a travel signature on my I-20 before my flight next week?"

Output (dict):
    office (str): registrar, international_student, financial_aid, it, housing or unknown.
    urgency (str): high, normal or low.
    reason (str): one short sentence that explains the choice.
    Sample: {"office": "international_student", "urgency": "high",
             "reason": "Travel signatures are given by International Student Services."}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/sorter.py      Score it: python3 score.py sorter
"""
import ollama

# This lets the file work both as "python3 llm/sorter.py" and as "from llm.sorter import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

OFFICES = ["registrar", "international_student", "financial_aid", "it", "housing", "unknown"]
URGENCIES = ["high", "normal", "low"]

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(message):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Question: {message}
Output:</query>"""
    return prompt


def classify(message):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: answer["office"] is in OFFICES, answer["urgency"] is in URGENCIES, and reason is a str.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. Return {"office": ..., "urgency": ..., "reason": ...}.
    raise NotImplementedError("classify is not written yet")


if __name__ == "__main__":
    message = input("Question: ")
    print(classify(message))
