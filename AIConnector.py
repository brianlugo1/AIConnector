from dotenv import load_dotenv
load_dotenv()

from queries import *
from ai import ai
from details import details
from usage import usage
from colorama import init, Fore
import os



def print_welcome_message():
    print(f"{Fore.CYAN}")
    print("------------------------------------------------")
    print("|         Welcome to AIConnector               |")
    print("|                                              |")
    print("|   I was created to help you connect with     |")
    print("|     ChatGPT or Perplexity and provide        |")
    print("|      insightful analytics about your         |")
    print("|               conversations!                 |")
    print("|                                              |")
    print("|   To ask ChatGPT a question simply type:     |")
    print("|       chatgpt                                |")
    print("|                                              |")
    print("|   To ask Perplexity a question simply type:  |")
    print("|       perplexity                             |")
    print("|                                              |")
    print("|   To view a detailed report type:            |")
    print("|       details                                |")
    print("|                                              |")
    print("|   To ask for help type:                      |")
    print("|       help or h                              |")
    print("|                                              |")
    print("------------------------------------------------")
    print()


def setup():
    init()
    os.system("clear")
    print_welcome_message()
    conn, cur = create_connection()
    create_table(conn, cur)
    return conn, cur


def ai_proc():
    conn, cur = setup()

    while True:
        messages = str(input(f"{Fore.BLUE}aicp{Fore.CYAN}$ {Fore.WHITE}"))

        if messages.find("exit")==0:break

        if messages.find("&&")!=-1:messages=messages.split("&&")

        else:messages=messages.split(";")

        for message in messages:
            message=message.strip()

            if message=="help" or message=="h" : usage("h")

            elif message=="clear": os.system("clear")

            elif message=="": pass

            elif message.find("chatgpt")==0 or message.find("perplexity")==0:
                if message=="chatgpt" or message=="perplexity":usage("o", message)

                else:
                    if message.find("chatgpt")==0:
                        ai(
                            "chatgpt", conn, cur,
                            message.replace("chatgpt ", "").replace("\'", "\"").lower().strip()
                        )

                    else:
                        ai(
                            "perplexity", conn, cur,
                            message.replace("perplexity ", "").replace("\'", "\"").lower().strip()
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

            else: usage(message)

    usage("e")

    cur.close()
    conn.close()

ai_proc()