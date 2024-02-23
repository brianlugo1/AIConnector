import os
from ai import ai
from queries import *
from usage import usage
from Constants import *
from details import details
from dotenv import load_dotenv
from colorama import init, Fore
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
    print(f"|       {GPT} or {GPT[0]}                           |")
    print("|                                              |")
    print("|   To ask Perplexity a question simply type:  |")
    print(f"|       {PER} or {PER[0]}                        |")
    print("|                                              |")
    print("|   To ask Llama a question simply type:       |")
    print(f"|       {LMA} or {LMA[0]}                             |")
    print("|                                              |")
    print("|   To view a detailed report type:            |")
    print(f"|       {DTS} or {DTS[0]}                           |")
    print("|                                              |")
    print("|   To ask for help type:                      |")
    print(f"|       {HLP} or {HLP[0]}                              |")
    print("|                                              |")
    print("------------------------------------------------\n")


def setup():
    init()

    load_dotenv()

    conn, cur=create_connection()

    if conn==None and cur==None:
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
        usage(usage=AI, ai=ai_cmd)
        return

    ai(ai_cmd, conn, cur, msg.strip())


def process_details_cmd(cur, cmd):
    if cmd=="":
        usage(usage=DTS)
        return

    if cmd.isnumeric():
        details(cur, cmd)
        return

    processed_cmd=cmd.split(" ")[0].lower()

    if len(processed_cmd)==1:

        for std_cmd in STD_FLGS_1ST_CHAR:
            if distance(std_cmd, processed_cmd)==0:
                details(cur, cmd)
                return

        usage(usage=DTS)

    else:
        min_dist=4

        process_details_cmd=""

        for std_cmd in STD_FLGS:
            dist=distance(cmd, std_cmd)

            if dist <= min_dist:
                min_dist=dist

                process_details_cmd=std_cmd

        if min_dist==0:
            if processed_cmd==DTE:
                processed_cmd=processed_cmd[:len(processed_cmd)]

                processed_cmd="d" + processed_cmd

                details(cur, processed_cmd)
                return

            details(cur, processed_cmd[:1])
            return

        if min_dist < 4:
            usage(usage=PRB, probable_command=f"{process_details_cmd}")
            return

        usage(usage=DTS)
        return


def exec_cmd(conn, cur, cmds):
    exit_code=0

    for cmd in cmds:
        cmd=cmd.strip()

        processed_cmd=cmd.split(" ")[0].lower()

        if processed_cmd=="":
            continue

        elif processed_cmd==HLP[0]:
            usage(usage=HLP)
            continue

        elif processed_cmd==GPT[0]:
            process_ai_cmd(conn, cur, cmd[1:].strip(), GPT)
            continue

        elif processed_cmd==PER[0]:
            process_ai_cmd(conn, cur, cmd[1:].strip(), PER)
            continue

        elif processed_cmd==LGT[0]:
            process_ai_cmd(conn, cur, cmd[1:].strip(), LMA)
            continue

        elif processed_cmd==DTS[0]:
            process_details_cmd(cur, cmd[1:].strip())
            continue

        elif processed_cmd=="cd":
            try:
                os.chdir(cmd[3:].strip())
                continue

            except:
                usage(usage=FLE, file_not_found=cmd[3:].strip())
                continue

        elif processed_cmd=="ls":
            os.system("ls")
            continue

        elif processed_cmd=="pwd":
            os.system("pwd")
            continue

        if len(processed_cmd) < 4:
            usage(command_not_found=processed_cmd)
            break

        min_dist=4

        probable_command=""

        for std_cmd in STD_CMDS:
            dist=distance(processed_cmd, std_cmd)

            if dist <= min_dist:
                min_dist=dist

                probable_command=std_cmd

        if probable_command==EXT and min_dist==0:
            exit_code=1
            break

        if min_dist==0:
            if probable_command==CLR:
                os.system(CLR)

            elif probable_command==HLP:
                usage(usage=HLP)

            elif probable_command==GPT:
                process_ai_cmd(conn, cur, cmd[GPT_LEN:].strip(), GPT)

            elif probable_command==PER:
                process_ai_cmd(conn, cur, cmd[PER_LEN:].strip(), PER)

            elif probable_command==LMA:
                process_ai_cmd(conn, cur, cmd[LMA_LEN:].strip(), LMA)

            elif probable_command==DTS:
                process_details_cmd(cur, cmd[DTS_LEN:].strip())

        elif min_dist==4:
            usage(command_not_found=f"{processed_cmd}")

        else:
            usage(usage=PRB, probable_command=f"{probable_command}")

    if exit_code:
        usage(usage=EXT)

    return exit_code