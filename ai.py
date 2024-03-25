import os
import time
from queries import *
from ollama import Client
from openai import OpenAI
from colorama import Fore
from format import *



"""
Description:
Given a target ai, a connection, a cursor, and a message,
ai() attempts to send an api request to the target ai with
the passed in message. ai() will query the db to check if
the message has been sent before to the target ai, thus
printing the stored response stored to save an unnecessary
api request. Otherwise, ai() will print the response from
the target ai, the time in seconds the target ai took to
respond, and store the target ai with the message and
response in the db.

Parameters:
ai: string (The name of the target ai)
conn: connection (The connection object returned from `psycopg2.connect()`)
cur: cursor (The cursor returned from `conn.cursor()`)
msg: string (The prompt message asked to the target ai)
"""
def ai(ai: str, conn, cur, msg: str):
    questions=search_question(
        cur,
        format_escape_single_and_double_quotes(msg),
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
            format_textwrap(completion["message"]["content"])
        else:
            format_textwrap(completion.choices[0].message.content)

        print()

        question=format_escape_single_and_double_quotes(msg)

        answer=""

        if ai==LMA:
            answer=format_escape_single_and_double_quotes(completion["message"]["content"])
        else:
            answer=format_escape_single_and_double_quotes(completion.choices[0].message.content)

        insert_conversation(conn, cur, question, answer, f"{toc - tic:0.2f}", ai)

    else:
        print("\nQuestion already asked:\n")

        print(format_divider())

        for question in questions:
            print('Stored answer:\n')

            format_textwrap(question[2])

            print(f"\nTime {Fore.GREEN}{question[6]}{Fore.WHITE} took to respond: {question[5]} seconds")

            print(f"Date asked: {question[4]}")

            print(f"Times asked: {question[3]+1}")

        print(format_divider())

        msg=format_escape_single_and_double_quotes(msg)

        increase_count_of_question(conn, cur, msg, ai)