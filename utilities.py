import os
from ai import ai
from queries import *
from usage import usage
from Constants import *
from colorama import Fore
from details import details
from dotenv import load_dotenv
from Levenshtein import distance



def print_welcome_message():
    print(f"{Fore.CYAN}")
    print("------------------------------------------------")
    print("|         Welcome to AIConnector               |")
    print("|                                              |")
    print("|   I was created to help you connect with     |")
    print("|   ChatGPT, Perplexity, Llama and provide     |")
    print("|      insightful analytics about your         |")
    print("|               conversations!                 |")
    print("|                                              |")
    print("|   To ask ChatGPT a question simply type:     |")
    print(f"|       {GPT} or c                           |")
    print("|                                              |")
    print("|   To ask Perplexity a question simply type:  |")
    print(f"|       {PER} or p                        |")
    print("|                                              |")
    print("|   To ask Llama a question simply type:       |")
    print(f"|       {LMA} or l                             |")
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
    load_dotenv()

    conn, cur = create_connection()

    if conn == None and cur == None:
        return None, None

    create_table(conn, cur)

    os.system(CLR)

    print_welcome_message()

    return conn, cur


def split_cmds(cmds):
    if cmds.find("&&") != -1:
        cmds=cmds.replace("&&", ";")

    return cmds.split(";")


def process_ai_cmd(conn, cur, msg, ai_cmd):
    if msg=="":
        usage(m="o", ai=ai_cmd)
        return

    ai(ai_cmd, conn, cur, msg.strip())


def process_details_cmd(cur, cmd):
    if cmd=="":
        usage(m="d")
        return

    if cmd.isnumeric():
        details(cur, cmd)
        return

    processed_cmd=cmd.split(" ")[0].lower()

    if len(processed_cmd) == 1:

        for s_cmd in STD_FLGS_1ST_CHAR:
            if distance(s_cmd, processed_cmd) == 0:
                details(cur, cmd)
                return

        usage(m="d")

    else:

        min_dist=4
        process_d_cmd=""

        for s_cmd in STD_FLGS:
            dist=distance(cmd, s_cmd)

            if dist <= min_dist:
                min_dist=dist
                process_d_cmd=s_cmd

        if min_dist == 0:
            if processed_cmd == DTE:
                processed_cmd=processed_cmd[:len(processed_cmd)]
                processed_cmd="d" + processed_cmd
                details(cur, processed_cmd)
                return

            details(cur, processed_cmd[:1])
            return

        if min_dist < 4:
            usage(m="p", probable_cmd=f"{process_d_cmd}")
            return

        usage(m="d")
        return


def exec_cmd(conn, cur, cmds):
    e=0

    for cmd in cmds:
        cmd=cmd.strip()

        processed_cmd=cmd.split(" ")[0].lower()

        if processed_cmd=="":
            continue
        elif processed_cmd=="h":
            usage(m="h")
            continue
        elif processed_cmd=="c":
            process_ai_cmd(conn, cur, cmd[1:].strip(), GPT)
            continue
        elif processed_cmd=="p":
            process_ai_cmd(conn, cur, cmd[1:].strip(), PER)
            continue
        elif processed_cmd=="l":
            process_ai_cmd(conn, cur, cmd[1:].strip(), LMA)
            continue
        elif processed_cmd=="d":
            process_details_cmd(cur, cmd[1:].strip())
            continue
        elif processed_cmd=="cd":
            try:
                os.chdir(cmd[3:].strip())
                continue
            except:
                usage(m="f", f_n_f=cmd[3:].strip())
                continue
        elif processed_cmd=="ls":
            os.system("ls")
            continue
        elif processed_cmd=="pwd":
            os.system("pwd")
            continue

        if len(processed_cmd) < 4:
            usage(m="", cmd_n_f=processed_cmd)
            break

        min_dist=4
        probable_cmd=""

        for s_cmd in STD_CMDS:
            dist=distance(processed_cmd, s_cmd)

            if dist <= min_dist:
                min_dist=dist
                probable_cmd=s_cmd

        if probable_cmd==EXT and min_dist==0:
            e=1
            break

        if min_dist==0:
            if probable_cmd==CLR:
                os.system(CLR)
            elif probable_cmd==HLP:
                usage(m="h")
            elif probable_cmd==GPT:
                process_ai_cmd(conn, cur, cmd[GPT_LEN:].strip(), GPT)
            elif probable_cmd==PER:
                process_ai_cmd(conn, cur, cmd[PER_LEN:].strip(), PER)
            elif probable_cmd==LMA:
                process_ai_cmd(conn, cur, cmd[LMA_LEN:].strip(), LMA)
            elif probable_cmd==DTS:
                process_details_cmd(cur, cmd[DTS_LEN:].strip())
        elif min_dist==4:
            usage(m="", cmd_n_f=f"{processed_cmd}")
        else:
            usage(m="p", probable_cmd=f"{probable_cmd}")

    if e:
        usage(m="e")

    return e