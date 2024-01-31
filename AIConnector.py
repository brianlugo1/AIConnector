import os
from ai import ai
from queries import *
from usage import usage
from details import details
from colorama import init, Fore
from Levenshtein import distance
from dotenv import load_dotenv
load_dotenv()



GPT = "chatgpt"
GPT_LEN = len(GPT)
PER = "perplexity"
PER_LEN = len(PER)
DTS = "details"
DTS_LEN = len(DTS)


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
    print(f"|       {GPT} or c                           |")
    print("|                                              |")
    print("|   To ask Perplexity a question simply type:  |")
    print(f"|       {PER} or p                        |")
    print("|                                              |")
    print("|   To view a detailed report type:            |")
    print(f"|       {DTS} or d                           |")
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


def split_cmd(cmds):
    if cmds.find("&&") != -1:
        cmds=cmds.replace("&&", ";")

    return cmds.split(";")


def process_ai_cmd(conn, cur, msg, ai_cmd):
    if msg=="":
        usage("o", ai_cmd)
        return

    ai(ai_cmd, conn, cur, msg.strip())


def process_details_cmd(cur, cmd):
    vaild_details_flag=False

    process_d_cmd=""

    if not cmd.isnumeric():
        process_d_cmd=cmd[:1].strip()

    if process_d_cmd=="t":
        vaild_details_flag=True
    elif process_d_cmd=="y":
        vaild_details_flag=True
    elif process_d_cmd=="a":
        vaild_details_flag=True
    elif process_d_cmd=="m":
        vaild_details_flag=True
    elif process_d_cmd=="l":
        vaild_details_flag=True
    elif process_d_cmd=="s":
        vaild_details_flag=True
    elif cmd.isnumeric():
        vaild_details_flag=True
    elif cmd.startswith("date"):
        vaild_details_flag=True
        cmd=cmd[4:]
        cmd="d"+cmd
    elif cmd.startswith("d"):
        vaild_details_flag=True

    if vaild_details_flag:
        if cmd.isnumeric() or cmd.startswith("d"):
            details(cur, cmd)
        else:
            details(cur, cmd[:1])
    else:
        usage("d")


def aicp():
    conn, cur=setup()

    while True:
        cmds=str(input(f"{Fore.BLUE}aicp{Fore.CYAN}$ {Fore.WHITE}"))

        cmds=split_cmd(cmds)

        e=0

        stored_cmds=[
            "exit",
            "help",
            "clear",
            GPT,
            PER,
            DTS,
        ]

        for cmd in cmds:
            cmd=cmd.strip()

            processed_cmd=cmd.split(" ")[0].lower()

            if processed_cmd=="":
                continue
            elif processed_cmd=="h":
                usage("h")
                continue
            elif processed_cmd=="c":
                process_ai_cmd(conn, cur, cmd[1:].strip(), GPT)
                continue
            elif processed_cmd=="p":
                process_ai_cmd(conn, cur, cmd[1:].strip(), PER)
                continue
            elif processed_cmd=="d":
                process_details_cmd(cur, cmd[1:].strip())
                continue
            elif processed_cmd=="cd":
                try:
                    os.chdir(cmd[3:].strip())
                    continue
                except:
                    usage("f", "", cmd[3:].strip())
                    continue
            elif processed_cmd=="ls":
                os.system("ls")
                continue
            elif processed_cmd=="pwd":
                os.system("pwd")
                continue

            min_dist=4
            probable_cmd=""

            for s_cmd in stored_cmds:
                dist=distance(processed_cmd, s_cmd)

                if dist <= min_dist:
                    min_dist=dist
                    probable_cmd=s_cmd

            if probable_cmd=="exit" and min_dist==0:
                e=1
                break

            if min_dist==0:
                if probable_cmd=="clear":
                    os.system("clear")
                elif probable_cmd=="help":
                    usage("h")
                elif probable_cmd==GPT:
                    process_ai_cmd(conn, cur, cmd[GPT_LEN:].strip(), GPT)
                elif probable_cmd==PER:
                    process_ai_cmd(conn, cur, cmd[PER_LEN:].strip(), PER)
                elif probable_cmd==DTS:
                    process_details_cmd(cur, cmd[DTS_LEN:].strip())
            elif min_dist==4:
                print(f"aicp: command not found: {processed_cmd}")
            else:
                print(f"aicp: did you mean to type {probable_cmd}?")

        if e:
            usage("e")
            break

aicp()