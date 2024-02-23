import textwrap
from queries import *
from usage import usage
from Constants import *
from colorama import Fore



def format_conversation(conversation):
    print("----------------------------------------------------------------------")

    print(f"Question: {conversation[1]}")

    print(f"\n{Fore.GREEN}{conversation[6]}{Fore.WHITE}:")

    for line in textwrap.wrap(conversation[2].replace("\"", "\'"), width=70):
        print(f"{line}")

    print("----------------------------------------------------------------------")


def format_conversations(conversations):
    print("-----------------------------------------------------------------------")

    print(f"|{ID}|{DATE}|{TIME}|{TIMEWAITED}|{AI}|")

    print("-----------------------------------------------------------------------")

    for conversation in conversations:
        id=str(conversation[0]).center(width, ' ')

        times_asked=str(conversation[3]).center(width, ' ')

        date_asked=str(conversation[4]).center(width, ' ')

        time_waited=str(conversation[5]).center(width, ' ')

        ai=str(conversation[6]).center(width, ' ')

        print(f"|{id}|{date_asked}|{times_asked}|{time_waited}|{ai}|")

    print("-----------------------------------------------------------------------")


def details(cur, flag):
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
    }

    if flag==TDY[0]:
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

        conversations=select_conversations_give_date(cur, date)

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