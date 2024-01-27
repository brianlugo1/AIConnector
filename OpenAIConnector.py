from dotenv import load_dotenv
load_dotenv()

from queries import *
from chatgpt import chatgpt
from details import details
from usage import usage
from colorama import init, Fore
import os


def openai_proc():
    init()
    os.system("clear")

    print(f"{Fore.CYAN}")
    print("------------------------------------------------")
    print("|         Welcome to OpenAIConnector           |")
    print("|                                              |")
    print("|   I was created to help you connect with     |")
    print("|   ChatGPT and provide insightful analytics   |")
    print("|   about your conversations with ChatGPT!     |")
    print("|                                              |")
    print("|   To ask ChatGPT a question simply type:     |")
    print("|       chatgpt                                |")
    print("|                                              |")
    print("|   To view a detailed report type:            |")
    print("|       details                                |")
    print("|                                              |")
    print("|   To ask for help type:                      |")
    print("|       help or h                              |")
    print("|                                              |")
    print("------------------------------------------------")
    print()

    conn, cur = create_connection()

    create_table(conn, cur)

    while True:
        print()
        messages = str(input(f"{Fore.BLUE}oaic{Fore.CYAN}$ {Fore.GREEN}"))
        print(f"{Fore.RED}")

        if messages.find("exit")!=-1:break

        if messages.find("&&")!=-1:messages=messages.split("&&")
        else:messages=messages.split(";")

        for message in messages:
            message=message.strip()
            if message=="help" or message=="h" : usage("h")
            elif message=="clear": os.system("clear")
            elif message=="": pass
            elif message.find("chatgpt")==0:
                if message=="chatgpt":usage("o")
                else: chatgpt(
                    conn, cur,
                    message.replace("chatgpt ", "").replace("\'", "\"").lower().strip()
                )
            elif message.find("details")==0:
                if message=="details": usage("d")
                else:
                    d=message.replace("details ", "")

                    if d=="t" or d=="today" or \
                       d=="y" or d=="yesterday" or \
                       d=="a" or d=="all" or \
                       d=="m" or d=="most" or \
                       d=="l" or d=="longest" or \
                       d=="s" or d=="shortest" or \
                       d.isnumeric() or \
                       d.find("date") == 0 : details(cur, d)
                    else: usage("d")
            else: print(f"oaic: command not found: {message}")

    print(f"{Fore.RED}exit")

    print()

    cur.close()
    conn.close()

openai_proc()