import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


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
            stop=["\n\n"],
        )
        return "1." + response["choices"][0]["text"]
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
            stop=["\n\n"],
        )
        return response["choices"][0]["text"]
    except:
        return ""
