import os
from flask import Flask, request, jsonify
from utils.ai import build_answers, build_questions
from utils.common import remove_leading
from utils.fetch import fetch_data
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST")
port = os.getenv("PORT")

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
    input = request.args.get("url")
    question = request.args.get("question")

    data = get_answer(input, question)
    return data


@app.route("/qa", methods=["GET"])
def qa():
    input = request.args.get("url")
    num = request.args.get("num", default=10)

    data = generate_qa(input, num)
    return data


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
