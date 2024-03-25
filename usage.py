from Constants import *
from colorama import Fore



def help_usage() -> None:
    """
    help_usage() prints out the information
    for supported commands.

    Paramters:
    None

    Returns:
    None
    """
    print(f"{Fore.RED}Usage: [options]\n")

    print("Options:")

    print(f"    {HLP[0]},       {HLP}: display this message")
    print(f"            {CLR}: clear the console")
    print(f"             {EXT}: exit OpenAIConnector\n")
    print(f"    {GPT[0]},    {GPT}: ask chatgpt a question")
    print(f"    {PER[0]}, {PER}: ask perplexity a question")
    print(f"    {LMA[0]},      {LMA}: ask llama a question")
    print(f"    {DTS[0]},    {DTS}: view details about existing conversations")


def ai_usage(ai: str) -> None:
    """
    ai_usage() prints out information for
    how to correctly run the command for
    interfacing with the target ai.

    Paramters:
    ai: string (The parsed target ai)

    Returns:
    None
    """
    print(f"{Fore.RED}Usage: {ai} {ai[:1]} [question]")


def details_usage() -> None:
    """
    details_usage() prints the information
    for all supported flags for details
    command.

    Paramters:
    None

    Returns:
    None
    """
    print(f"{Fore.RED}Usage: {DTS} {DTS[0]} [options]\n")

    print("Options:")

    print(f"    {TDY[0]},       {TDY}: display a report for {TDY}'s conversations")
    print(f"    {YTD[0]},   {YTD}: display a report for {YTD}'s conversations")
    print(f"    {ALL[0]},         {ALL}: display a report for {ALL} conversations")
    print(f"    {MST[0]},        {MST}: display a report for the {MST} asked conversation")
    print(f"    {LGT[0]},     {LGT}: display a report for the conversation that took the {LGT}")
    print(f"    {SRT[0]},    {SRT}: display a report for the conversation that took the {SRT}")
    print("              [id]: display the report for the conversation with the given id")
    print(f"    {DTE[0]}, {DTE} [{DTE}]: display the report for the conversation with the given {DTE}")
    print("                     (expected format: YYYY-MM-DD)")


def details_date_usage() -> None:
    """
    details_date_usage() prints out the
    information for how to use the date
    flag for details command.

    Paramters:
    None

    Returns:
    None
    """
    print(f"{Fore.RED}Usage: {DTS} {DTE} {DTE[0]} [YYYY-DD-MM]")


def exit_message() -> None:
    """
    exit_message() prints out the exit message.

    Paramters:
    None

    Returns:
    None
    """
    print(f"{Fore.RED}exit")


def command_not_found_usage(m: str) -> None:
    """
    command_not_found_usage() prints out
    information about the unknown parsed
    command.

    Paramters:
    m: string (The unknown parsed command)

    Returns:
    None
    """
    print(f"{Fore.RED}aicp: command not found: {m}")


def file_not_found_usage(m) -> None:
    """
    file_not_found_usage() prints out
    information about the unknown parsed
    file or directory.

    Paramters:
    m: string (The unknown file or directory parsed)

    Returns:
    None
    """
    print(f"{Fore.RED}aicp: no such file or directory: {m}")


def probable_command_usage(m: str) -> None:
    """
    probable_command_usage() prints out
    information about the probable command
    meant to be typed.

    Paramters:
    m: string (The probable command)

    Returns:
    None
    """
    print(f"aicp: did you mean to type {m}?")


def usage(usage: str="", ai: str="", file_not_found: str="", probable_command: str="", command_not_found: str="") -> None:
    """
    usage() calls the corresponding functions
    for the given flag and passes the passed
    in parsed paramters.

    Paramters:
    usage: string (The usage flag)
    ai: string (The parsed target ai)
    file_not_found: string (The unknown parsed file or directory)
    probable_command: string (The probable command)
    command_not_found: string (The unknown parsed command)

    Returns:
    None
    """
    if usage==HLP:
        help_usage()

    elif usage==AI:
        ai_usage(ai)

    elif usage==DTS:
        details_usage()

    elif usage==DTE:
        details_date_usage()

    elif usage==EXT:
        exit_message()

    elif usage==FLE:
        file_not_found_usage(file_not_found)

    elif usage==PRB:
        probable_command_usage(probable_command)

    else:
        command_not_found_usage(command_not_found)