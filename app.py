import os
from flask import Flask, request, jsonify
from services import get_answer, get_answer_v2, generate_qa
from utils.fetch import fetch_data
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/ama", methods=["GET"])
def ama():
    url = request.args.get("url")
    all = request.args.get("all", default=False)
    tag = request.args.get("tag", default="p")
    question = request.args.get("question")

    data = get_answer(url, all, tag, question)
    return data


@app.route("/ama_v2", methods=["GET"])
def ama_v2():
    url = request.args.get("url")
    all = request.args.get("all", default=False)
    tag = request.args.get("tag", default="p")
    text = request.args.get("text")
    question = request.args.get("question")

    data = get_answer_v2(url, all, tag, text, question)
    return data


@app.route("/qa", methods=["GET"])
def qa():
    url = request.args.get("url")
    all = request.args.get("all", default=False)
    tag = request.args.get("tag", default="p")
    num = request.args.get("num", default=10)

    data = generate_qa(url, all, tag, num)
    return data


@app.route("/fetch", methods=["GET"])
def fetch():
    url = request.args.get("url")
    all = request.args.get("all", default=False)
    tag = request.args.get("tag", default="p")

    data = fetch_data(url, all, tag)
    return data


@app.route('/')
def index():
    return jsonify({"Message": "Welcome!"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
