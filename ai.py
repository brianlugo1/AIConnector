from colorama import init, Fore
from openai import OpenAI
from queries import *
import textwrap
import time
import os



def ai(ai, conn, cur, m):
    init()
    print(f"{Fore.YELLOW}")

    questions=search_question(cur, m, ai)

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

        print(f"{ai} responded in: {toc - tic:0.2f} seconds")

        print()

        for line in textwrap.wrap(completion.choices[0].message.content):
            print(line)

        print()

        insert_conversation(
            conn, cur, m,
            completion.choices[0].message.content.replace("\'", "\""),
            f"{toc - tic:0.2f}", ai
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

            print(f"Time {question[6]} took to respond: {question[5]} seconds")
            print(f"Date asked: {question[4]}")
            print(f"Times asked: {question[3]+1}")

        print("--------------------------------------------------")

        print()

        increase_count_of_question(conn, cur, m, ai)
