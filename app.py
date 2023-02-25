import os
from flask import Flask, request, jsonify
from utils.ai import build_answers, build_questions
from utils.common import remove_leading
from utils.fetch import fetch_data
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST")
port = os.getenv("PORT", default=5000)

app = Flask(__name__)


def get_answer(url, question):
    context = fetch_data(url)
    print(context)

    answer = build_answers(context, question)
    print("\nanswers\n" + answer)

    return jsonify({"question": question, "answer": answer})


def generate_qa(url, num):
    context = fetch_data(url)
    print(context)

    questions = build_questions(context, num)
    print("\nquestions\n" + questions)

    answers = "1." + build_answers(context, questions)
    print("\nanswers\n" + answers)

    keys = questions.split("\n")
    values = answers.split("\n")
    dictionary = [{'question': remove_leading(key),
                   'answer': remove_leading(value)} for key, value in zip(keys, values)]

    return jsonify(dictionary)


@app.route("/ama", methods=["GET"])
def ama():
    url = request.args.get("url")
    question = request.args.get("question")

    data = get_answer(url, question)
    return data


@app.route("/qa", methods=["GET"])
def qa():
    url = request.args.get("url")
    num = request.args.get("num", default=10)

    data = generate_qa(url, num)
    return data


@app.route("/fetch", methods=["GET"])
def fetch():
    url = request.args.get("url")

    data = fetch_data(url)
    return data


if __name__ == '__main__':
    app.run(debug=True, port=port)
