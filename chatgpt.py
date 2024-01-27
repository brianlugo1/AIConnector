from colorama import init, Fore
from openai import OpenAI
from queries import *
import textwrap
import time
import os



def chatgpt(conn, cur, m):
    init()
    print(f"{Fore.YELLOW}")

    questions=search_question(cur, m)

    if len(questions)==0:
        tic=time.perf_counter()

        client = OpenAI(
            api_key=os.environ.get("OPEN_API_KEY"),
        )

        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': m,
                }
            ],
        )

        toc=time.perf_counter()

        print(f"ChatGPT responded in: {toc - tic:0.2f} seconds")

        print()

        for line in textwrap.wrap(completion.choices[0].message.content):
            print(line)

        print()

        insert_conversation(
            conn, cur, m,
            completion.choices[0].message.content.replace("\'", "\""),
            f"{toc - tic:0.2f}"
        )

    else:
        print()

        print("Question already asked:")

        print()

        print("--------------------------------------------------")

        for question in questions:
            answer=question[2].replace("\"", "\'")

            print('Stored answer:')

            print()

            for line in textwrap.wrap(answer):
                print(f"{line}")

            print()

            print(f"Time ChatGPT took to respond: {question[5]} seconds")
            print(f"Date asked: {question[4]}")
            print(f"Times asked: {question[3]+1}")

        print("--------------------------------------------------")

        print()

        increase_count_of_question(conn, cur, m)
