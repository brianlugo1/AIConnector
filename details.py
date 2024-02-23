import textwrap
from queries import *
from usage import usage
from colorama import Fore



def format_conversation(conversation):
    question=conversation[1]
    answer=conversation[2]
    ai=conversation[6]

    print("----------------------------------------------------------------------")
    print(f"Question: {question}")

    print(f"\n{Fore.GREEN}{ai}{Fore.WHITE}:")

    for line in textwrap.wrap(answer.replace("\"", "\'"), width=70):
        print(f"{line}")

    print("----------------------------------------------------------------------")


def format_conversations(conversations):
    width=13

    ID="ID".center(width, ' ')
    TIME="Times Asked".center(width, ' ')
    DATE="Date Asked".center(width, ' ')
    TIMEWAITED="Time Waited".center(width, ' ')
    AI="AI".center(width, ' ')

    print("-----------------------------------------------------------------------")
    print(f"|{ID}|{TIME}|{DATE}|{TIMEWAITED}|{AI}|")
    print("-----------------------------------------------------------------------")

    for conversation in conversations:
        id=str(conversation[0]).center(width, ' ')
        times_asked=str(conversation[3]).center(width, ' ')
        date_asked=str(conversation[4]).center(width, ' ')
        time_waited=str(conversation[5]).center(width, ' ')
        ai=str(conversation[6]).center(width, ' ')

        print(f"|{id}|{date_asked}|{times_asked}|{time_waited}|{ai}|")
    print("-----------------------------------------------------------------------")


def details(cur, m):
    conversations=[]

    title={
        "t": "Here is a report of today's conversations:",
        "y": "Here is a report of yesterday's conversations:",
        "a": "Here is a report of all conversations:",
        "m": "Here is the most asked question:",
        "l": "Here is the question that took the longest:",
        "s": "Here is the question that took the shortest:",
        "i": f"Here is the conversation with the id [{m}]",
        "d": f"Here is the conversations with the given date [{m[1:].strip()}]",
    }

    if m=="t":
        conversations=select_questions_asked(cur, "t")
    elif m=="y":
        conversations=select_questions_asked(cur, "y")
    elif m=="a":
        conversations=select_questions_asked(cur, "a")
    elif m=="m":
        conversations=select_most_asked_question(cur)
    elif m=="l":
        conversations=select_longest_question_waited_for(cur)
    elif m=="s":
        conversations=select_shortest_question_waited_for(cur)
    elif m.isnumeric():
        conversations=select_conversation_given_id(cur, m)

    elif m.startswith("d"):
        date=""
        date=m[1:].strip()

        m="d"

        year_month_day=date.split("-")

        if len(year_month_day) != 3:
            usage(m="dd")
            return

        if len(year_month_day[0]) != 4:
            usage(m="dd")
            return

        if len(year_month_day[1]) != 2:
            usage(m="dd")
            return

        if len(year_month_day[2]) != 2:
            usage(m="dd")
            return

        conversations=select_conversations_give_date(cur, date)

    id=""

    if m.isnumeric():
        id=m
        m="i"

    print(title[m])

    if len(conversations)==0:
        if m.isnumeric():
            print(f"No Conversation with id [{id}]")

        else:
            print("No Conversations to show!")

    elif len(conversations)==1 and m=="i":
        format_conversation(conversations[0])

    else:
        format_conversations(conversations)