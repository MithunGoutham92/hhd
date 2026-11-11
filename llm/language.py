"""HHD.E Language: finds the language of a student's question and translates it to English.

Function: to_english(text)

Input:
    text (str): the question, in any language.
    Sample: "¿Cuál es la fecha límite para la FAFSA?"

Output (dict):
    language (str): the language name in English, such as "English", "Spanish" or "Korean".
    english_text (str): the question in English (the same text if it is already English).
                        UW names such as FAFSA, MyUW, Register.UW, Duo and I-20 stay exactly the same.
    Sample: {"language": "Spanish", "english_text": "What is the deadline for the FAFSA?"}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/language.py      Score it: python3 score.py language
"""
import ollama

# This lets the file work both as "python3 llm/language.py" and as "from llm.language import ...".
if __package__:
    from .utils import read_json
else:
    from utils import read_json

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(text):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Question: {text}
Output:</query>"""
    return prompt


def to_english(text):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. build_prompt(...), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json.
    # 2. Check it: language is a str, and english_text is a str that is not empty. Ask for the two keys language and english_text.
    #    Ask again (up to 3 tries) if it fails, then raise ValueError.
    # 3. If the language is English, english_text is the question exactly as written. Return {"language": ..., "english_text": ...}.
    raise NotImplementedError("to_english is not written yet")


if __name__ == "__main__":
    text = input("Question: ")
    print(to_english(text))
