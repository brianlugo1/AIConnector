from colorama import init, Fore
from queries import *
from usage import usage
import textwrap



def details(cur, m):
    init()
    print(f"{Fore.MAGENTA}")

    conversations=[]

    if m=="t" or m=="today":
        print("Here is a report of today's conversations:")

        conversations=select_questions_asked(cur, "t")
    elif m=="y" or m=="yesterday":
        print("Here is a report of yesterday's conversations:")

        conversations=select_questions_asked(cur, "y")
    elif m=="a" or m=="all":
        print("Here is a report of all conversations:")

        conversations=select_questions_asked(cur, "a")
    elif m=="m" or m=="most":
        print("Here is the most asked question:")

        conversations=select_most_asked_question(cur)
    elif m=="l" or m=="longest":
        print("Here is the question that took the longest:")

        conversations=select_longest_question_waited_for(cur)
    elif m=="s" or m=="shortest":
        print("Here is the question that took the shortest:")

        conversations=select_shortest_question_waited_for(cur)
    elif m.isnumeric():
        print(f"Here is the conversation with the id [{m}]")

        conversations=select_conversation_given_id(cur, m)
    elif m.find("date") == 0:
        m=m.replace("date", "").strip()

        d=m.split("-")

        if m=="" or len(d) != 3 or len(d[0]) != 4 or len(d[1]) != 2 or len(d[2]) != 2:
            print(f"{Fore.RED}")
            usage("dd")
            return

        print(f"Here is the conversations with the given date [{m}]")

        conversations=select_conversations_give_date(cur, m)

    print()

    print("--------------------------------------------------")

    print()

    if len(conversations)==0:
        if m.isnumeric():print(f"No Conversation with id [{m}]")
        else:print("No Conversations to show!")

        print()

    for conversation in conversations:
        print(f"Question:                                      [{conversation[0]}]")

        for line in textwrap.wrap(conversation[1].replace("\"", "\'"), width=50):
            print(f"{line}")

        print()

        print("Answer: ")

        stored_message=conversation[2].replace("\"", "\'")

        if stored_message.find('```') != -1:
            stored_message=stored_message.split('```')

            for index in range(1, len(stored_message)):
                if index%2==1:
                    for line in textwrap.wrap(stored_message[index-1], width=50):
                        print(f"{line}")
                else:
                    print(stored_message[index-1])

                print()

        else:
            for line in textwrap.wrap(stored_message, width=50):
                print(f"{line}")

            print()

        print(f"Time ChatGPT took to respond: {conversation[5]} seconds")
        print(f"Date asked: {conversation[4]}")
        print(f"Times asked: {conversation[3]}")

        print()

    print("--------------------------------------------------")

    print()
