import os
import time
import textwrap
from queries import *
from ollama import Client
from openai import OpenAI
from colorama import Fore



def ai(ai, conn, cur, msg):
    questions=search_question(
        cur,
        msg.replace("\'", "\\\'").replace("\"", "\\\""),
        ai
    )

    if len(questions)==0:
        tic=time.perf_counter()

        api_key="CHATGPT_API_KEY"

        base_url=None

        model="gpt-3.5-turbo"

        if ai==PER:
            api_key="PERPLEXITY_API_KEY"

            base_url="https://api.perplexity.ai"

            # Available Models: Mistral 7B, Llama 13B, Code Llama 34B, Llama 70B
            model="mistral-7b-instruct"

        client=[]

        completion=[]

        if ai==LMA:
            client=Client(host="http://127.0.0.1:11434")

            completion=client.chat(
                model=f"{LMA}2",
                messages=[
                    {
                        'role': 'user',
                        'content': msg,
                    }
                ]
            )

        else:
            client=OpenAI(
                api_key=os.environ.get(api_key),
                base_url=base_url
            )

            completion=client.chat.completions.create(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': msg,
                    }
                ],
            )

        toc=time.perf_counter()

        print(f"{Fore.GREEN}{ai}{Fore.WHITE} responded in: {toc - tic:0.2f} seconds\n")

        if ai==LMA:
            for line in textwrap.wrap(completion["message"]["content"]):
                print(line.strip())
        else:
            for line in textwrap.wrap(completion.choices[0].message.content):
                print(line)

        print()

        question=msg.replace("\'", "\\\'").replace("\"", "\\\"")

        answer=""

        if ai==LMA:
            answer=completion["message"]["content"].replace("\'", "\\\'").replace("\"", "\\\"")
        else:
            answer=completion.choices[0].message.content.replace("\'", "\\\'").replace("\"", "\\\"")

        insert_conversation(conn, cur, question, answer, f"{toc - tic:0.2f}", ai)

    else:
        print("\nQuestion already asked:\n")

        print("--------------------------------------------------")

        for question in questions:
            print('Stored answer:\n')

            for line in textwrap.wrap(question[2]):
                print(f"{line}")

            print(f"\nTime {Fore.GREEN}{question[6]}{Fore.WHITE} took to respond: {question[5]} seconds")
            print(f"Date asked: {question[4]}")
            print(f"Times asked: {question[3]+1}")

        print("--------------------------------------------------\n")

        msg=msg.replace("\'", "\\\'").replace("\"", "\\\"")

        increase_count_of_question(conn, cur, msg, ai)