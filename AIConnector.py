#!/usr/bin/env python3

import readline

from utilities import (
    setup,
    split_cmds,
    exec_cmd
)

from colorama import Fore
from AutoCompleter import MyCompleter



def aicp() -> None:
    """
    aicp() envokes a connection to the postgresql server
    hosting our db and starts the forever while loop
    reading in commands. Each read in command is parsed
    and an attempt is made to execute each parsed
    command. If an attempt to execute a command returns
    a 0, then the while loop terminates. Before exiting,
    aicp() closes the opened connection to the
    postgresql server.

    Parameters:
    None

    Returns:
    None
    """
    conn, cur=setup()

    if conn==None and cur==None:
        print("An error occurred connecting to the PostgreSQL server. Is the PostgreSQL server running?")
        return

    while True:
        cmds=str(input(f"{Fore.BLUE}aicp{Fore.CYAN}$ {Fore.WHITE}"))

        cmds=split_cmds(cmds)

        if exec_cmd(conn, cur, cmds):
            break

    conn.close()


readline.set_completer(MyCompleter([]).complete)

readline.parse_and_bind("tab: complete")

readline.parse_and_bind("bind -v")

readline.parse_and_bind("bind ^I rl_complete")


aicp()
