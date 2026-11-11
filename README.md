# HuskyHelpDesk

Husky Help Desk answers UW students' questions from UW office policies. A student writes in any language. The assistant translates the question, hides personal details, chooses the office, drafts an answer from the policy, removes sentences the policy does not support, and lists deadlines and fees.

## What the assistant does

`python3 main.py` sends each question through the tools in this order:

1. **Language** (`to_english`): finds the language and translates the question to English.
2. **Privacy** (`redact`): hides names, student numbers, phone numbers and email addresses.
3. **Sorter** (`classify`): chooses the UW office and the urgency.
4. **Reply** (`draft_policy_answer`, team file): chooses one of that office's policies in
   `data/policies.json` and drafts an answer from it.
5. **Fact Checking** (`check_answer`): checks each sentence of the answer against the policy.
   A sentence the policy does not support is marked "left out".
6. **Details** (`extract`): lists the deadlines, fees and documents in the policy.
7. The answer is shown with the policy's web page. Nothing is saved.

Each tool is one function in one file in `llm/`. When every tool works, the whole assistant works.
`main.py` stops at the first tool that is not written yet and says "Not ready yet", so in Phase 1 you test
your own tool on its own (see "Test and score your tool").

## Get the code

1. On this project's GitHub page, click the green **Code** button, then **Download ZIP**.
2. Unzip the file. You get a folder whose name ends in `-main`, such as `HuskyHelpDesk-main`.
   On Windows, "Extract All" can put it inside a second folder with the same name: use the folder that has `main.py` in it.
3. In VS Code, choose **File > Open Folder...** and pick that folder. The VS Code Terminal then starts in it.
   Run every command from this folder.

## Set up

1. Install Ollama from https://ollama.com and open it. It must be running whenever you use the project.
2. In the Terminal, run `ollama pull llama3.2`. This downloads the model (about 2 GB), once.
3. Install the Python package: `python3 -m pip install -r requirements.txt`.
4. Check it: run `python3 main.py`. It starts and waits for you to type. Until the tools are written, it says
   "Not ready yet" for anything you type. Type `quit` to stop.

On Windows, type `py` where this README says `python3`. For example: `py -m pip install -r requirements.txt`.

## Your work, step by step

Use your own file and tool name where this list says `llm/sorter.py` and `sorter`.

1. Do "Get the code" and "Set up" above.
2. Find your role in "Find your file". Open your tool file and read its docstring.
3. Read your role in "Your role" below. It says what score.py checks and gives tips.
4. In your tool file, write the four prompt parts (`instruction`, `context`, `examples`, `output_format`).
   They start as TODO.
5. Follow the TODO comments in your function. Write the code, then delete the `raise NotImplementedError` line.
6. Run `python3 llm/sorter.py` and try your function on one input.
7. Run `python3 score.py sorter given`. Change your prompt and code until most of the 10 given
   cases pass.
8. Write your 30 test cases in your cases file (see the section "Write 30 test cases of your own"), then run
   `python3 score.py sorter` for the score out of 40.
9. Save your tool file and your cases file. Phase 2 then joins every tool in `main.py`.

## Find your file

Find your role in the table. You change two files: you write your function in your tool file, and you write
30 test cases in your cases file. **Do not change any other file.**

| Role | Your tool file | Write this function | Your cases file | Score it |
|---|---|---|---|---|
| HHD.A Sorter | `llm/sorter.py` | `classify` | `data/my_cases/sorter.json` | `python3 score.py sorter` |
| HHD.B Privacy | `llm/privacy.py` | `redact` | `data/my_cases/privacy.json` | `python3 score.py privacy` |
| HHD.C Fact Checking | `llm/fact_check.py` | `check_answer` | `data/my_cases/fact_check.json` | `python3 score.py fact_check` |
| HHD.D Details | `llm/details.py` | `extract` | `data/my_cases/details.json` | `python3 score.py details` |
| HHD.E Language | `llm/language.py` | `to_english` | `data/my_cases/language.json` | `python3 score.py language` |

## What is in your file

Open your file. From top to bottom it has:

1. **The docstring**, the text between the `"""` marks at the top: the inputs, the
   output and a sample of each. Do not change the function name, its inputs or the keys of its output,
   because `main.py` and `score.py` use them.
2. **The import lines.** The `if __package__:` lines let the file run on its own and from `main.py`.
   Leave them as they are. To use one more function from `utils.py`, add its name to both import lines.
3. **Four prompt parts**: `instruction`, `context`, `examples` and `output_format`. Each one says TODO. Write them.
4. **`build_prompt`**: already written. It puts the four parts and the input into one prompt. Do not change it.
5. **Your function.** It has TODO comments with the steps, and `raise NotImplementedError(...)`.
   Write the function, then delete the `raise NotImplementedError` line.
6. **A small test** at the bottom, under `if __name__ == "__main__":`. Some tests ask you to type an input.

You may add your own helper functions to your file, and you may import more from `utils.py`.

## How every tool works

Every tool follows the same steps:

1. Make the prompt: `prompt = build_prompt(...)`, with your function's inputs.
2. Call the LLM:
   `output = ollama.generate(model="llama3.2", prompt=prompt, format="json", options={"num_predict": 500})`.
   `format="json"` makes the LLM answer in JSON. `num_predict` stops an answer that runs on too long.
3. Turn the answer into a dict: `answer = read_json(output.response)`. If the answer is not complete JSON,
   you get `{}`.
4. Check the answer: are all the keys there, and are the values allowed (for example, a word from your list)?
   If not, ask again. Use a `while` loop that stops after 3 tries.
5. If the 3rd answer is still not usable, `raise ValueError("...")` with a short message. `main.py` then says
   "Sorry, we couldn't process this" and saves nothing.

Some tools need more than one LLM call, or code that does part of the work. The TODO comments in your
function and the tips for your role below say how.

## Your role

### HHD.A Sorter: `llm/sorter.py`

Write `classify(message)`. It gets the English question, with personal details hidden, and returns `{"office": ..., "urgency": ..., "reason": ...}`.

- **score.py passes a given case when** `office` is the one in the answer key.
- **Your cases** (`data/my_cases/sorter.json`): `question`: a student's question in English. `office`: one of the words in `OFFICES`.
- **Tip:** `OFFICES` and `URGENCIES` at the top of your file list the allowed words. Say in `context` what each office handles. `unknown` is for a question that no office here handles.
- **Tip:** Check that office and urgency are words from those lists. If not, ask again.

### HHD.B Privacy: `llm/privacy.py`

Write `redact(text)`. It gets the English question and returns `{"redacted_text": ..., "items_hidden": ...}`.

- **score.py passes a given case when** both tests work. Test 1 is the question alone: every UW term in it (such as MyUW or FAFSA) must still be there. Test 2 adds a made-up contact line (Jordan Example, a student number and an email): those must be gone, and the UW terms must still be there.
- **Your cases** (`data/my_cases/privacy.json`): `text`: a question with made-up personal details in it (or none). `must_hide`: every name, student number, phone number and email in the text, copied exactly. `must_keep`: the UW terms that must stay, such as "MyUW". score.py runs `redact` once on `text`: nothing in `must_hide` may be left, and every word of `must_keep` must stay.
- **Tip:** Do not ask the LLM to rewrite the text, because it changes other words too. Ask it to list the items it finds, one list for each key of `PLACEHOLDERS`, plus a list of uw_terms (UW offices, websites and systems). Your code then replaces each item in the text with its `PLACEHOLDERS` value.
- **Tip:** The LLM often lists things that are not personal details, such as "Someone" or a UW system such as Duo. Your code should skip them. `NOT_NAMES` at the top of your file is a start, and the TODO comments in your function list more cases.

### HHD.C Fact Checking: `llm/fact_check.py`

Write `check_answer(answer, policy_text)`. It gets a draft answer and the policy it must be based on, and returns `{"status": ..., "checks": [...]}`, with one check for each sentence.

- **score.py passes a given case when** the status of every sentence is the one in the answer key, and the overall status is right. score.py gives your tool answers with known results, so you can work before the Reply team file is written.
- **Your cases** (`data/my_cases/fact_check.json`): `answer`: a draft answer. `policy_text`: the policy it must be based on (copy one from `data/policies.json`, or from a UW web page). `statuses`: one for each sentence of the answer, `"supported"` or `"unsupported"`.
- **Tip:** Check one sentence at a time: `split_sentences` in `utils.py` splits the answer.
- **Tip:** A sentence copied word for word from the policy is supported. Your code can find this without the LLM.
- **Tip:** `STATUSES` lists the two words the LLM may give.

### HHD.D Details: `llm/details.py`

Write `extract(policy_text)`. It gets a **policy**, not the student's question, and returns `{"deadlines": [...], "fees": [...], "required_documents": [...]}`.

- **score.py passes a given case when** every deadline and fee in the answer key is in your lists, and every deadline and fee in your lists is in the policy, word for word.
- **Your cases** (`data/my_cases/details.json`): `policy_text`: a policy (from a UW web page, for example). `deadlines` and `fees`: every date and dollar amount in it that a student needs, copied word for word.
- **Tip:** `KEYS` at the top of your file lists the three keys.
- **Tip:** Ask the LLM to copy dates and dollar amounts exactly. Your code can check that each one is in `policy_text`, and leave out or ask again for the ones that are not.

### HHD.E Language: `llm/language.py`

Write `to_english(text)`. It gets the question as the student wrote it and returns `{"language": ..., "english_text": ...}`.

- **score.py passes a given case when** an English question is found as English and any other question as not English, and every UW name in the question (such as FAFSA or I-20) is still in `english_text`.
- **Your cases** (`data/my_cases/language.json`): `question`: a question in any language. `language`: its language, such as "English" or "Korean". `keep`: UW names that must stay the same in the English text, such as "FAFSA".
- **Tip:** Say in `context` that UW names such as FAFSA, MyUW, Register.UW, Duo and I-20 stay exactly the same.
- **Tip:** If the question is in English, return it exactly as the student wrote it.

## Write 30 test cases of your own

The 10 given cases in `data/cases.json` are only a start. Write 30 more for your tool, so that it is
tested on 40 cases.

1. Open your cases file, such as `data/my_cases/sorter.json`. It starts with one sample case.
   Change the sample, or replace it with your own.
2. Add your cases after it. Each case is `{ ... }` with the fields that "Your role" lists for your
   tool. Put a comma between two cases. The file looks like this:

```json
[
  {
    "question": "My Duo app stopped working after I got a new phone. How can I log in to MyUW?",
    "office": "it",
    "note": "Sample case: change it or replace it with your own."
  },
  {
    "question": "...",
    "office": "..."
  }
]
```

3. Run `python3 score.py sorter mine` (with your tool's name). score.py first checks your file. If a
   case has a missing field or a wrong value, it tells you which one and scores nothing until you fix it.

Rules for good test cases:

- Decide the right answer for each case before you run your tool. Never change an answer to match
  what your tool says.
- Cover every office, and make at least a quarter of your cases hard: cases where a careless
  tool would go wrong.
- Do not copy your test cases, or the 10 given cases, into the `examples` of your prompt.
  A test shows something only if the tool has not seen the answer.
- Personal details must be made up. Use phone numbers from 555-0100 to 555-0199 and email addresses that end in @example.com: they are kept for examples.
- score.py does not use the fields `source` and `note`. Use `note` to say why a case is hard.

## Team files (Phase 2)

In Phase 2 the whole team writes these files together. Do not change them in Phase 1.
They have TODO steps, like the role files.

- `llm/reply.py`: `draft_policy_answer(question, policies)` returns `{"answer": ..., "policy": ...}`: an answer from one policy, and that policy (or None).

## Test and score your tool

Use your own tool's name in these commands.

- `python3 llm/sorter.py`: runs the small test at the bottom of your tool file.
- `python3 score.py sorter`: runs your tool on the 10 given cases, then on your own cases.
  Each case prints PASS or FAIL and what your tool returned. At the end you see the score on the given
  cases, the score on yours, and the total, such as `Score: 34 of 40`.
- `python3 score.py sorter given` or `python3 score.py sorter mine`: only the given cases,
  or only yours.
- `python3 score.py sorter 3` runs given case 3, and `python3 score.py sorter mine 3` runs
  your case 3. One case is quicker while you change your prompt.
- An LLM does not give the same answer every time. Run score.py two or three times before you decide that a
  change made your prompt better.

What the messages mean:

- `data/my_cases/... is not valid JSON ... on line 5`: look for a missing comma, quote mark or bracket on that
  line or the line before it. JSON needs double quotes, and `true`, `false` and `null` in small letters.
- `data/my_cases/... has mistakes`: the list under it says which of your cases has a missing field or a
  wrong value.
- `... is not written yet`: your function still has `raise NotImplementedError`.
- `FAIL  error: ...`: your function stopped with an error on that case. If it is your ValueError, the LLM gave
  3 answers your code could not use: make `output_format` and `examples` clearer.
- `Failed to connect to Ollama`: open the Ollama app, then try again.
- `model "llama3.2" not found`: run `ollama pull llama3.2`.
- `No module named 'ollama'`: do step 3 of "Set up".

To try another local model, download it with `ollama pull <name>` (the names are on https://ollama.com/search)
and change `model="llama3.2"` in your file. Score both models and compare.

## Files you do not change

- `llm/utils.py` (utils is short for utilities): functions that every tool can use. `load_data(name)` and `load_text(name)` read a file in `data/`, `save_data(name, data)` writes one, `split_sentences(text)` gives a list of sentences, and `read_json(text)` turns the LLM's answer into a dict (`{}` if the answer is not complete JSON).
- `llm/__init__.py`: makes `llm/` a package, so `main.py` can import your tool.
- `score.py`: checks your tool on the given cases and on yours.
- `main.py`: joins all the tools.
- `data/`: the given cases and the data that `main.py` saves. In `data/my_cases/`, change only your own cases file.

## Run the whole assistant

`python3 main.py`. Type a question, `demo` to send the 10 test questions, or `quit`.

## Data

- `data/cases.json`: 10 labelled test questions, used by score.py
- `data/policies.json`: 10 short UW policies (two for each office), with their web pages
- `data/my_cases/`: one cases file for each tool, such as `data/my_cases/sorter.json`. Each starts with one sample; students add their own.

## Licence and sources

Each policy is a short summary in our own words of a UW office web page (the URL is in policies.json), checked 2026-11-09. Dates are for 2026-27. The questions and draft answers were written for this project.

## Notes

- Three test questions are in Chinese, Spanish and Korean; the other seven are in English.
- Each Privacy test adds a made-up contact line (Jordan Example, a student number, jordan@example.com). Privacy is also tested on the question alone: UW names such as MyUW must not be hidden.
- This project uses the local model llama3.2. Every call has `options={"num_predict": 500}`, so an answer that
  runs on too long stops instead of hanging your program.
