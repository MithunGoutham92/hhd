"""Husky Help Desk: joins the five tools into one assistant that answers UW students from policy text.

Run from the project folder:  python3 main.py
Type a question, "demo" to send the 10 questions in data/cases.json, or "quit" to stop.
The policies are in data/policies.json. This assistant does not browse the web.
"""
from llm.details import extract
from llm.fact_check import check_answer
from llm.language import to_english
from llm.privacy import redact
from llm.reply import draft_policy_answer
from llm.sorter import classify
from llm.utils import load_data


def office_policies(office):
    policies = []
    for policy in load_data("policies.json"):
        if policy["office"] == office:
            policies.append(policy)
    return policies


def handle_question(message):
    """Runs one question through every tool and prints a checked answer."""
    english = to_english(message)
    redacted = redact(english["english_text"])
    question = redacted["redacted_text"]
    sorted_question = classify(question)
    print(f"[{english['language']} | {sorted_question['office']} | {sorted_question['urgency']}]")

    policies = office_policies(sorted_question["office"])
    if not policies:
        print("Please contact the UW office that handles this question.")
        return
    draft = draft_policy_answer(question, policies)
    if draft["policy"] is None:
        print("Please contact the office. No policy here answers this question.")
        return

    # Keep only the sentences that Fact Checking says the policy supports.
    checked = check_answer(draft["answer"], draft["policy"]["text"])
    for check in checked["checks"]:
        if check["status"] == "supported":
            print("- " + check["claim"])
        else:
            print("- [left out, not in the policy] " + check["claim"])

    details = extract(draft["policy"]["text"])
    for key in ["deadlines", "fees", "required_documents"]:
        if details[key]:
            print(key.replace("_", " ").capitalize() + ": " + ", ".join(details[key]))
    print("Source: " + draft["policy"]["title"] + ", " + draft["policy"]["url"])


def run(message):
    try:
        handle_question(message)
    except NotImplementedError as error:
        print("Not ready yet:", error)
    except (ValueError, ConnectionError) as error:
        print("Sorry, we couldn't process this. Please try again.", error)


def main():
    print("Husky Help Desk. Type a question, demo, or quit.")
    while True:
        message = input("\n> ").strip()
        if message.lower() in ("quit", "exit"):
            break
        if not message:
            continue
        if message.lower() == "demo":
            for case in load_data("cases.json")["cases"]:
                print("\n> " + case["message"])
                run(case["message"])
            continue
        run(message)


if __name__ == "__main__":
    main()
