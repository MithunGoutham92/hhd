"""HHD.C Fact Checking: checks each sentence of a draft answer against the UW policy text.

Function: check_answer(answer, policy_text)

Input:
    answer (str): the draft answer in English.
    policy_text (str): the policy text the answer must be based on.
    Sample: "An official transcript costs $13. You can pick it up at the office.",
            "An official transcript costs $13 for each copy. Paper transcripts can no longer be picked up."

Output (dict):
    status (str): supported if every sentence is supported, otherwise needs_review.
    checks (list of dict): one for each sentence, with:
        claim (str): the sentence.
        status (str): supported if the policy states the same fact, otherwise unsupported.
    Sample: {"status": "needs_review",
             "checks": [{"claim": "An official transcript costs $13.", "status": "supported"},
                        {"claim": "You can pick it up at the office.", "status": "unsupported"}]}

Raises ValueError if the LLM's answer can't be used.
Test it: python3 llm/fact_check.py      Score it: python3 score.py fact_check
"""
import ollama

# This lets the file work both as "python3 llm/fact_check.py" and as "from llm.fact_check import ...".
if __package__:
    from .utils import split_sentences, read_json
else:
    from utils import split_sentences, read_json

STATUSES = ["supported", "unsupported"]

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(sentence, policy_text):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Policy: {policy_text}
Sentence: {sentence}
Output:</query>"""
    return prompt


def check_answer(answer, policy_text):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. Split the answer with split_sentences.
    # 2. For each sentence: a sentence copied word for word from the policy is supported (no LLM call).
    #    Otherwise build_prompt(sentence, policy_text), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json. Ask for one key, status, with a word from STATUSES.
    #    Ask again (up to 3 tries) if it is not in STATUSES, then raise ValueError.
    # 3. The overall status is "supported" only if every sentence is supported, otherwise "needs_review".
    # 4. Return {"status": ..., "checks": [...]}, one dict for each sentence.
    # A helper function such as check_sentence(sentence, policy_text) keeps check_answer short.
    raise NotImplementedError("check_answer is not written yet")


if __name__ == "__main__":
    answer = input("Answer: ")
    policy = "An official transcript costs $13 for each copy. Paper transcripts can no longer be picked up."
    print(check_answer(answer, policy))
