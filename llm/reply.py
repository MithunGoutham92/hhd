"""Phase 2 team tool: drafts an answer to a student's question from UW policy text.

Function: draft_policy_answer(question, policies)

Input:
    question (str): the student's question in English, with personal details hidden.
    policies (list of dict): the policies of the chosen office, each with title, text and url.
    Sample: "How much is an official transcript?",
            [{"title": "Official transcripts", "url": "https://...",
              "text": "An official transcript costs $13 for each copy. ..."}]

Output (dict):
    answer (str): two or three short sentences, using only facts from one policy.
                  The LLM first chooses the policy, then answers from that policy only.
    policy (dict): the policy the answer is based on, so Fact Checking can check it.
    Sample: {"answer": "An official transcript costs $13 for each copy.", "policy": {...}}

Raises ValueError if the LLM's answer can't be used.
"""
import ollama

if __package__:
    from .utils import read_json
else:
    from utils import read_json

instruction = """TODO: say who the LLM is and what it must do."""

context = """TODO: the labels, rules and facts the LLM needs."""

examples = """TODO: a few examples of input and the exact output you want."""

output_format = """TODO: the exact JSON the LLM must return."""


def build_prompt(question, policy):
    prompt = f"""<instruction>{instruction}</instruction>
<context>{context}</context>
<examples>{examples}</examples>
<output_format>{output_format}</output_format>
<query>Policy: {policy["text"]}
Question: {question}
Output:</query>"""
    return prompt


def draft_policy_answer(question, policies):
    # TODO: write this function. The docstring at the top of this file is the contract.
    # 1. First choose the policy that answers the question: one more LLM call with your own prompt
    #    that lists the policies with numbers and asks for the number (0 if none fits). If none fits,
    #    return {"answer": "Please contact the office.", "policy": None}.
    # 2. build_prompt(question, policy), call
    #    ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500}),
    #    and read the answer with read_json. Ask for one key, answer. Ask again (up to 3 tries) if it
    #    is missing or empty, then raise ValueError.
    # 3. Return {"answer": ..., "policy": policy}.
    # A helper function such as choose_policy(question, policies) keeps this short.
    raise NotImplementedError("draft_policy_answer is not written yet")


if __name__ == "__main__":
    policies = [{"title": "Official transcripts", "url": "https://registrar.washington.edu/transcripts/pt-faqs/",
                 "text": "An official transcript costs $13 for each copy."}]
    print(draft_policy_answer("How much is an official transcript?", policies))
