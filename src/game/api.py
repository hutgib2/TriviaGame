import html
import json
import sys

async def fetchTriviaQuestions(amount):
    # fetch data from api
    url = f'https://opentdb.com/api.php?amount={amount}&type=multiple'

    # if in browser, use browser-supported fetch
    if sys.platform == "emscripten":
        import platform
        try:
            async with platform.fopen(url, "r") as f:
                data = json.loads(f.read())
        except Exception as e:
            print(f"Failed to fetch trivia questions: {e}")
            return []
    else:
        try:
            import requests
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Failed to fetch trivia questions: {e}")
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