import requests
import json
import html

url = "https://opentdb.com/api.php?amount=50&type=multiple"
response = requests.get(url)
data = response.json()
new_questions = data["results"]

for q in new_questions:
    q["question"] = html.unescape(q["question"])
    q["correct_answer"] = html.unescape(q["correct_answer"])
    q["category"] = html.unescape(q["category"])
    q["incorrect_answers"] = [html.unescape(ans) for ans in q["incorrect_answers"]]

old_questions = []
try:
    with open('assets/trivia.json', 'r') as file:
        old_questions = json.load(file)
except:
    print("file empty")

with open('assets/trivia.json', 'w', encoding='utf-8') as file:
    old_questions += new_questions
    json.dump(old_questions, file, indent=4, ensure_ascii=False)
