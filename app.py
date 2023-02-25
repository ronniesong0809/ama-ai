from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
load_dotenv()
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
port = os.getenv("PORT")

app = Flask(__name__)

def fetch_data(url):
  r = requests.get(url)
  print(r.status_code)
  soup = BeautifulSoup(r.text, "html.parser")
  if (r.status_code == 200):
    strs = []
    for node in soup.findAll('p'):
      strs.append(node.findAll(string=True))
    page = ''.join(str(s) for s in strs)
    return page
  else:
    return ''

def build_questions(context, num):
  try:
    response = openai.Completion.create(
      engine="davinci-instruct-beta-v3",
      prompt=os.getenv("QUESTION_PROMPT").format(num, context),
      temperature=0,
      max_tokens=257,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n\n"]
    )
    return '1.' + response['choices'][0]['text']
  except:
    return ""

def build_answers(context, questions):
  try:
    response = openai.Completion.create(
      engine="davinci-instruct-beta-v3",
      prompt=os.getenv("ANSWER_PROMPT").format(context, questions),
      temperature=0,
      max_tokens=257,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n\n"]
    )
    return response['choices'][0]['text']
  except:
    return ""

def get_answer(url, question):
  context = fetch_data(url)
  print(context)

  answer = build_answers(context, question)
  print("\nanswers\n" + answer)
  keys = question.split('\n')
  values = answer.split('\n')
  dictionary = dict(zip(keys, values))
  
  return jsonify(dictionary)

def generate_qa(url, num):
  context = fetch_data(url)
  print(context)

  questions = build_questions(context, num)
  print("\nquestions\n" + questions)

  answers = '1.' + build_answers(context, questions)
  print("\nanswers\n" + answers)
  keys = questions.split('\n')
  values = answers.split('\n')
  dictionary = dict(zip(keys, values))
  
  return jsonify(dictionary)

@app.route("/ama", methods=["GET"])
def ama():
  input = request.args.get('url')
  question = request.args.get('question')

  data = get_answer(input, question)
  return data

@app.route("/qa", methods=["GET"])
def qa():
  input = request.args.get('url')
  num = request.args.get('num')

  data = generate_qa(input, num)
  return data

if __name__ == '__main__':
  app.run(host='localhost', port=port, debug=True)
