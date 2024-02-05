from colorama import init, Fore
from openai import OpenAI
from ollama import Client
from queries import *
import textwrap
import time
import os



def ai(ai, conn, cur, m):
    init()

    questions=search_question(
        cur,
        m.replace("\'", "\\\'").replace("\"", "\\\""),
        ai
    )

    if len(questions)==0:
        tic=time.perf_counter()

        api_key="CHATGPT_API_KEY"
        base_url=None
        model="gpt-3.5-turbo"

        if ai=="perplexity":
            api_key="PERPLEXITY_API_KEY"
            base_url="https://api.perplexity.ai"

            # Available Models: Mistral 7B, Llama 13B, Code Llama 34B, Llama 70B
            model="mistral-7b-instruct"

        client = []
        completion = []

        if ai=="llama":
            client = Client(host="http://127.0.0.1:11434")

            completion = client.chat(
                model="llama2",
                messages=[
                    {
                        'role': 'user',
                        'content': m,
                    }
                ]
            )

        else:
            client = OpenAI(
                api_key=os.environ.get(api_key),
                base_url=base_url
            )

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': m,
                    }
                ],
            )

        toc=time.perf_counter()

        print(f"{Fore.GREEN}{ai}{Fore.WHITE} responded in: {toc - tic:0.2f} seconds")

        print()

        if ai == "llama":
            for line in textwrap.wrap(completion["message"]["content"]):
                print(line.strip())
        else:
            for line in textwrap.wrap(completion.choices[0].message.content):
                print(line)

        print()

        q=m.replace("\'", "\\\'").replace("\"", "\\\"")

        a=""

        if ai == "llama":
            a=completion["message"]["content"].replace("\'", "\\\'").replace("\"", "\\\"")
        else:
            a=completion.choices[0].message.content.replace("\'", "\\\'").replace("\"", "\\\"")

        insert_conversation(conn, cur, q, a, f"{toc - tic:0.2f}", ai)

    else:
        print()

        print("Question already asked:")

        print()

        print("--------------------------------------------------")

        for question in questions:
            answer=question[2]

            print('Stored answer:')

            print()

            for line in textwrap.wrap(answer):
                print(f"{line}")

            print()

            print(f"Time {Fore.GREEN}{question[6]}{Fore.WHITE} took to respond: {question[5]} seconds")
            print(f"Date asked: {question[4]}")
            print(f"Times asked: {question[3]+1}")

        print("--------------------------------------------------")

        print()

        m=m.replace("\'", "\\\'").replace("\"", "\\\"")

        increase_count_of_question(conn, cur, m, ai)
