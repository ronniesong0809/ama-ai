from flask import jsonify
from utils.ai import build_answers, build_questions
from utils.common import remove_leading
from utils.fetch import fetch_data


def get_answer(url, all, tag, question):
    context = fetch_data(url, all, tag)
    print(context)

    answer = build_answers(context, question)
    print("\nanswers\n" + answer)

    return jsonify({"question": question, "answer": answer})


def get_answer_v2(url, all, tag, text, question):
    context = fetch_data(url, all, tag)
    context.append(text)
    print(context)

    answer = build_answers(context, question)
    print("\nanswers\n" + answer)

    return jsonify({"question": question, "answer": answer})


def generate_qa(url, all, tag, num):
    context = fetch_data(url, all, tag)
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
