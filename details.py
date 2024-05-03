from queries import *
from usage import usage
from Constants import *
from colorama import Fore
from format import *



def format_conversation(conversation: list) -> None:
    """
    format_conversation() prints the stored prompt
    message, target ai, and response to the console.

    Parameters:
    conversation: list (The list of attributes for a given conversation to print)

    Returns:
    None
    """
    print(format_divider())

    print(f"Question:")

    format_textwrap(conversation[1])

    print(f"\n{Fore.GREEN}{conversation[6]}{Fore.WHITE}:")

    format_textwrap(conversation[2])

    print(format_divider())


def format_conversations(conversations: list[list]) -> None:
    """
    format_conversations() prints a table with a
    header of column names and all of the stored
    ids, dates, times asked, and target ai.

    Paramters:
    conversations: list[list] (A list of lists of attributes of given conversations to print)

    Returns:
    None
    """
    print(format_divider())

    print(f"|{ID}|{DATE}|{TIME}|{TIMEWAITED}|{AIC}|")

    print(format_divider())

    for conversation in conversations:
        id=format_column(conversation[0])

        times_asked=format_column(conversation[3])

        date_asked=format_column(conversation[4])

        time_waited=format_column(conversation[5])

        ai=format_column(conversation[6])

        print(f"|{id}|{date_asked}|{times_asked}|{time_waited}|{ai}|")

    print(format_divider())


def details(cur, flag: str) -> None:
    """
    details() takes the parsed flag and attemps
    to query the db for stored conversations
    that satisfy the given flag. details() then
    prints the stored conversations that satisfy
    the given flag.

    Parameters:
    cur: cursor (The cursor object returned from `conn.cursor()`)
    flag: string (The parsed flag for filtering stored conversations)

    Returns:
    None
    """
    conversations=[]

    title={
        TDY[0]: f"Here is a report of {TDY}'s conversations:",
        YTD[0]: f"Here is a report of {YTD}'s conversations:",
        ALL[0]: f"Here is a report of {ALL} conversations:",
        MST[0]: f"Here is the {MST} asked question:",
        LGT[0]: f"Here is the question that took the {LGT}:",
        SRT[0]: f"Here is the question that took the {SRT}:",
        "i": f"Here is the conversation with the id [{flag}]",
        DTE[0]: f"Here is the conversations with the given {DTE} [{flag[1:].strip()}]",
        AI: f"Here is the conversations with the given {AI}"
    }

    flag=flag.lower()

    if flag.startswith(AI):
        ai = flag[2:].strip()

        if ai=="":
            usage(usage=(DTE+AI))
            return
        
        if ai==GPT[0]:
            ai=GPT
        
        if ai==PER[0]:
            ai=PER

        if ai==LMA[0]:
            ai=LMA

        flag=AI

        conversations=select_conversations_given_ai(cur, ai)

    elif flag==TDY[0]:
        conversations=select_questions_asked(cur, TDY[0])

    elif flag==YTD[0]:
        conversations=select_questions_asked(cur, YTD[0])

    elif flag==ALL[0]:
        conversations=select_questions_asked(cur, ALL[0])

    elif flag==MST[0]:
        conversations=select_most_asked_question(cur)

    elif flag==LGT[0]:
        conversations=select_longest_question_waited_for(cur)

    elif flag==SRT[0]:
        conversations=select_shortest_question_waited_for(cur)

    elif flag.isnumeric():
        conversations=select_conversation_given_id(cur, flag)

    elif flag.startswith(DTE[0]):
        date=flag[1:].strip()

        flag=DTE[0]

        year_month_day=date.split("-")

        if len(year_month_day) != 3:
            usage(usage=DTE)
            return

        if len(year_month_day[0]) != 4:
            usage(usage=DTE)
            return

        if len(year_month_day[1]) != 2:
            usage(usage=DTE)
            return

        if len(year_month_day[2]) != 2:
            usage(usage=DTE)
            return

        conversations=select_conversations_given_date(cur, date)

    id=""

    if flag.isnumeric():
        id=flag

        flag="i"

    print(title[flag])

    if len(conversations)==0:
        if flag.isnumeric():
            print(f"No Conversation with id [{id}]")

        else:
            print("No Conversations to show!")

    elif len(conversations)==1 and flag=="i":
        format_conversation(conversations[0])

    else:
        format_conversations(conversations)