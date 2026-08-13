import asyncio
import html
import json
import sys
import urllib.error
import urllib.request

if sys.platform == "emscripten":
    import platform


def _fetch_sync(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read())


async def fetchTriviaQuestions(amount):
    url = f'https://opentdb.com/api.php?amount={amount}&type=multiple'

    try:
        if sys.platform == "emscripten":
            async with platform.fopen(url, "r") as f:
                data = json.loads(f.read())
        else:
            data = await asyncio.to_thread(_fetch_sync, url)
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"Failed to fetch trivia questions: {e}")
        return []

    if data.get("response_code") != 0:
        print(f"API returned no questions (code {data.get('response_code')})")
        return []
    
    # removing html encoding 
    questions = data["results"] # this is a list
    for q in questions:
        q["question"] = html.unescape(q["question"])
        q["correct_answer"] = html.unescape(q["correct_answer"])
        q["category"] = html.unescape(q["category"])
        q["incorrect_answers"] = [html.unescape(ans) for ans in q["incorrect_answers"]]

    # filter out questions with long answers
    def answers_fit_in_button(q):
        all_answers = [q["correct_answer"], *q["incorrect_answers"]]
        return all(len(ans.split()) <= 5 for ans in all_answers)

    questions = [q for q in questions if answers_fit_in_button(q)]

    return questions