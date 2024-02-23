from Constants import *
from colorama import Fore



def help_usage():
    print(f"{Fore.RED}Usage: [options]\n")

    print("Options:")

    print(f"    {HLP[0]},       {HLP}: display this message")
    print(f"            {CLR}: clear the console")
    print(f"             {EXT}: exit OpenAIConnector\n")
    print(f"    {GPT[0]},    {GPT}: ask chatgpt a question")
    print(f"    {PER[0]}, {PER}: ask perplexity a question")
    print(f"    {LMA[0]},      {LMA}: ask llama a question")
    print(f"    {DTS[0]},    {DTS}: view details about existing conversations")


def ai_usage(ai):
    print(f"{Fore.RED}Usage: {ai} {ai[:1]} [question]")


def details_usage():
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


def details_date_usage():
    print(f"{Fore.RED}Usage: {DTS} {DTE} {DTE[0]} [YYYY-DD-MM]")


def exit_message():
    print(f"{Fore.RED}exit")


def command_not_found_usage(m):
    print(f"{Fore.RED}aicp: command not found: {m}")


def file_not_found_usage(m):
    print(f"{Fore.RED}aicp: no such file or directory: {m}")


def probable_command_usage(m):
    print(f"aicp: did you mean to type {m}?")


def usage(usage="", ai="", file_not_found="", probable_command="", command_not_found=""):
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