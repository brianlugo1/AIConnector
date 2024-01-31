from colorama import init, Fore



def help_usage():
    print(f"{Fore.RED}Usage: [options]\n")
    print("Options:")
    print("    h,       help: display this message")
    print("            clear: clear the console")
    print("             exit: exit OpenAIConnector\n")
    print("    c,    chatgpt: ask chatgpt a question")
    print("    p, perplexity: ask perplexity a question")
    print("    d,    details: view details about existing conversations")


def ai_usage(ai):
    print(f"{Fore.RED}Usage: {ai} {ai[:1]} [question]")


def details_usage():
    print(f"{Fore.RED}Usage: details d [options]\n")
    print("Options:")
    print("    t,       today: display a report for today's conversations")
    print("    y,   yesterday: display a report for yesterday's conversations")
    print("    a,         all: display a report for all conversations")
    print("    m,        most: display a report for the most asked conversation")
    print("    l,     longest: display a report for the conversation that took the longest")
    print("    s,    shortest: display a report for the conversation that took the shortest")
    print("              [id]: display the report for the conversation with the given id")
    print("    d, date [date]: display the report for the conversation with the given date")
    print("                     (expected format: YYYY-MM-DD)")


def details_date_usage():
    print(f"{Fore.RED}Usage: details date d [YYYY-DD-MM]")


def exit_message():
    print(f"{Fore.RED}exit")


def command_not_found(m):
    print(f"{Fore.RED}aicp: command not found: {m}")


def file_not_found(m):
    print(f"{Fore.RED}aicp: no such file or directory: {m}")


def probable_command(m):
    print(f"aicp: did you mean to type {m}?")


def usage(m="", ai = "", f_n_f="", probable_cmd="", cmd_n_f=""):
    init()

    if m=="h":
        help_usage()
    elif m=="o":
        ai_usage(ai)
    elif m=="d":
        details_usage()
    elif m=="dd":
        details_date_usage()
    elif m=="e":
        exit_message()
    elif m=="f":
        file_not_found(f_n_f)
    elif m=="p":
        probable_command(probable_cmd)
    else:
        command_not_found(cmd_n_f)
