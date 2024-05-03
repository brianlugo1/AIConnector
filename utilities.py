import os
from ai import ai
from queries import *
from usage import usage
from Constants import *
from details import details
from dotenv import load_dotenv
from colorama import init
from Levenshtein import distance
from format import *
from typing import Tuple
import requests



def setup() -> Tuple | Tuple[None, None]:
    """
    setup() initializes colorama, loads enviornment variables,
    and attempts to create a connection to postgresql server.
    If the attempt to connect to the postgresql server fails,
    a tuble of None, None is returned. setup() then creates
    the table in the db. setup() then clears the console and
    returns the conn and cur objects.

    Parameters:
    None

    Returns:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)
    """
    init()

    load_dotenv()

    conn, cur=create_connection()

    if conn==None and cur==None:
        return None, None

    create_table(conn, cur)

    os.system(CLR)

    return conn, cur


def split_cmds(cmds: str) -> list[str]:
    """
    split_cmds() replaces any instances of
    the text `&&` with `;` and returns a
    list of parsed commands split on the
    occurrences of `;`.

    Parameters:
    cmds: string (The parsed string of commands)

    Returns:
    cmds.split(";"): list[str] (The list of parsed commands)
    """
    if cmds.find("&&") != -1:
        cmds=cmds.replace("&&", ";")

    return cmds.split(";")


def parse_ai_flags(msg: str, ai_cmd: str) -> str | None:
    """
    parse_ai_flags() attempts to parse
    the ai flag that can either be:

    f [filename] -> Specify the filename
    to parse and append to prompt message.

    or

    l [link] -> Specify the link of a webpage
    to parse and append to the prompt message.

    Then attempts to add the contents of
    the file or url with the prompt
    message.

    Parameters:
    msg: string (The ai flags with prompt message asked to the target ai)
    msg: string (The target ai)

    Returns:
    new_msg: string (The prompt message with the specified file or url contents)
    or
    None
    """
    cmd_args = msg.split(" ")

    file_contents = ""

    url_contents = ""

    first_arg_found = False

    first_arg = cmd_args[0]

    first_arg_filename = ""

    first_arg_url = ""

    if first_arg == FLE[0] or first_arg == FLE:
        if len(cmd_args) < 2:
            usage(usage=AI, ai=ai_cmd)
            return

        first_arg_found = True

        first_arg_filename = cmd_args[1]

        try:
            with open(first_arg_filename, 'r') as f:
                file_contents = f.read()

        except:
            usage(usage=FLE, file_not_found=first_arg_filename)
            return

    if first_arg == LNK[0] or first_arg == LNK:
        if len(cmd_args) < 2:
            usage(usage=AI, ai=ai_cmd)
            return

        first_arg_found = True

        first_arg_url = cmd_args[1]

        if not first_arg_url.startswith("https://"):
            first_arg_url = "https://" + first_arg_url

        try:
            response = requests.get(first_arg_url, timeout=STANDARD_TIMEOUT)

            response.raise_for_status()

            url_contents = response.text

        except:
            usage(usage=LNK, link_not_found=first_arg_url)
            return

    if first_arg_found:
        cmd_args = cmd_args[2:]
    
    if len(cmd_args) == 0:
        usage(usage=AI, ai=ai_cmd)
        return

    new_msg = " ".join(cmd_args)

    if file_contents:
        new_msg += f" Filename: {first_arg_filename}, File Contents: {file_contents}"

    if url_contents:
        new_msg += f" Url: {first_arg_url}, Url Contents: {url_contents}"

    return new_msg



def process_ai_cmd(conn, cur, msg: str, ai_cmd: str) -> None:
    """
    process_ai_cmd() calls usage() with the
    flag of AI constant column string and
    the target ai if no prompt message is
    passed. Otherwise calls parse_ai_flags()
    and ai() with the parsed prompt message
    and target ai.

    Parameters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)
    msg: string (The prompt message asked to the target ai)
    ai_cmd: string (The target ai)

    Returns:
    None
    """
    if msg=="":
        usage(usage=AI, ai=ai_cmd)
        return

    new_msg = parse_ai_flags(msg, ai_cmd)

    if new_msg == None:
        return

    ai(ai_cmd, conn, cur, msg.strip(), new_msg.strip())


def process_details_cmd(cur, cmd: str) -> None:
    """
    process_details_cmd() confirms that valid
    flags are passed to details command. Otherwise
    process_details_cmd() attempts to determine
    which flag is passed and envoke target logic.
    If passed in parsed flags do not match stored
    flags for details command, then the stored
    command that is the closest in terms of
    insertions, deletions, and replacements is
    returned. Otherwise process_details_cmd()
    calls usage() with the parsed flag.

    Parameters:
    cur: cursor (The cursor object returned from `conn.cursor()`)
    cmd: string (The parsed details command)

    Returns:
    None
    """
    if cmd=="":
        usage(usage=DTS)
        return

    if cmd.isnumeric():
        details(cur, cmd)
        return

    processed_cmd=cmd.split(" ")[0].lower()

    if len(processed_cmd)==1:
        for std_cmd in STD_FLGS_1ST_CHAR:
            if std_cmd == processed_cmd:
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


def exec_cmd(conn, cur, cmds: str) -> int:
    """
    exec_cmd() attempts to parse the passed in
    command and confirms if the parsed command
    is valid. If true, exec_cmd() envokes
    target logic to execute parsed command.
    Otherwise calls usage() with the
    corresponding parsed command and flags.
    If a parsed command does not match to a
    stored command, the closest matching
    command is passed to usage(). If the
    `exit` command is parsed, the variable
    `exit_code` is set to 1 and returned.
    Otherwise exec_cmd() returns a 0.

    Parameters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)
    cmds: string (The parsed command)

    Returns:
    exit_code: integer (Either a 1 or 0 for whether the `exit` command is parsed)
    """
    exit_code=0

    for cmd in cmds:
        cmd=cmd.strip()

        processed_cmd=cmd.split(" ")[0].lower()

        if processed_cmd=="":
            continue

        elif processed_cmd==WLC[0]:
            usage(usage=WLC)
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

            elif probable_command==WLC:
                usage(usage=WLC)

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