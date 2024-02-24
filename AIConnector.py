import readline

from utilities import (
    setup,
    split_cmds,
    exec_cmd
)

from colorama import Fore
from AutoCompleter import MyCompleter



def aicp():
    conn, cur=setup()

    if conn==None and cur==None:
        print("An error occurred connecting to the PostgreSQL server. Is the PostgreSQL server running?")
        return

    while True:
        cmds=str(input(f"{Fore.BLUE}aicp{Fore.CYAN}$ {Fore.WHITE}"))

        cmds=split_cmds(cmds)

        if exec_cmd(conn, cur, cmds):
            break


readline.set_completer(MyCompleter([]).complete)

readline.parse_and_bind("tab: complete")

readline.parse_and_bind("bind -v")

readline.parse_and_bind("bind ^I rl_complete")


aicp()