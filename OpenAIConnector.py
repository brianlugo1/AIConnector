from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import textwrap
import datetime
import psycopg2
import time
import os

def create_connection():
    conn = psycopg2.connect("dbname=openai")
    cur = conn.cursor()
    return conn, cur

def create_table(conn, cur):
    cur.execute("CREATE TABLE IF NOT EXISTS conversation (\
        id serial PRIMARY KEY, \
        question varchar UNIQUE NOT NULL, \
        answer varchar NOT NULL, \
        count integer NOT NULL, \
        day date NOT NULL, \
        duration real NOT NULL\
    );")

    conn.commit()

def delete_table(conn, cur):
    cur.execute("DROP TABLE IF EXISTS conversation;")

    conn.commit()

def clear_table(conn, cur):
    cur.execute("TRUNCATE conversation;")

    conn.commit()

def select_table_names(cur):
    cur.execute("SELECT * FROM pg_catalog.pg_tables \
        WHERE schemaname='public';\
    ")

    return cur.fetchall()

def select_table_columns(cur):
    cur.execute("SELECT * FROM information_schema.columns \
        WHERE table_name='conversation';\
    ")

    return cur.fetchall()

def print_table_details(cur):
    print("Details about Table:")
    print()
    print("Name:   ", select_table_names(cur)[0][1])

    for table in select_table_columns(cur):
        print("Column: ", table[3], "( Type: ", table[7], ")")

    print()

def select_all_conversations(cur):
    cur.execute("\
        SELECT * FROM conversation;\
    ")

    return cur.fetchall()

def insert_conversation(conn, cur, question, answer, seconds):
    cur.execute(f"INSERT INTO conversation (\
            question, answer, count, \
            day, duration\
        ) VALUES (\
            \'{question}\', \'{answer}\', 1, \
            \'{datetime.datetime.now().date()}\', \
            {seconds}\
        );\
    ")

    conn.commit()

def delete_conversation(conn, cur, question, answer):
    cur.execute(f"DELETE FROM conversation \
        WHERE conversation.question=\'{question}\' \
        AND conversation.answer=\'{answer}\';\
    ")

    conn.commit()

def search_question(cur, question):
    cur.execute(f"SELECT * FROM conversation \
        WHERE conversation.question=\'{question}\';\
    ")

    return cur.fetchall()

def increase_count_of_question(conn, cur, question):
    cur.execute(f"UPDATE conversation \
        SET count = count+1 \
        WHERE conversation.question=\'{question}\';\
    ")

    conn.commit()

def select_questions_asked(cur, d):
    day=""

    if d=="t": day=datetime.datetime.now().date()
    elif d=="y":
        day=datetime.datetime.now().date().replace(
            day=datetime.datetime.now().date().day-1
        )

    elif d=="a": return select_all_conversations(cur)

    cur.execute(f"SELECT * FROM conversation \
        WHERE conversation.day=\'{day}\';\
    ")

    return cur.fetchall()

def select_most_asked_question(cur):
    cur.execute(f"""
        SELECT * FROM conversation
        WHERE count=(
            SELECT MAX(count)
            FROM conversation
        );
    """)

    return cur.fetchall()

def select_longest_question_waited_for(cur):
    cur.execute(f"SELECT * FROM conversation \
        WHERE duration=(\
            SELECT MAX(duration) \
            FROM conversation\
        );\
    ")

    return cur.fetchall()

def select_shortest_question_waited_for(cur):
    cur.execute(f"SELECT * FROM conversation \
        WHERE duration=(\
        SELECT MIN(duration) FROM conversation\
    );")

    return cur.fetchall()

def select_conversation_given_id(cur, id):
    cur.execute(f"SELECT * FROM conversation \
        WHERE id={id};\
    ")

    return cur.fetchall()

def select_conversations_give_date(cur, date):
    cur.execute(f"SELECT * FROM conversation \
        WHERE day=\'{date}\';\
    ")

    return cur.fetchall()

def chatgpt(conn, cur, m):
    questions=search_question(cur, m)

    if len(questions)==0:
        tic=time.perf_counter()

        client = OpenAI(
            api_key=os.environ.get("OPEN_API_KEY"),
        )

        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': m,
                }
            ],
        )

        toc=time.perf_counter()

        print(f"ChatGPT responded in: {toc - tic:0.2f} seconds")

        print()

        for line in textwrap.wrap(completion.choices[0].message.content):
            print(line)

        print()

        insert_conversation(
            conn, cur, m,
            completion.choices[0].message.content.replace("\'", "\""),
            f"{toc - tic:0.2f}"
        )
    else:
        print()
        print("Question already asked:")
        print()
        print("--------------------------------------------------")

        for question in questions:
            answer=question[2].replace("\"", "\'")

            print('Stored answer:')
            print()

            for line in textwrap.wrap(answer):
                print(f"{line}")

            print()
            print(f"Time ChatGPT took to respond: {question[5]} seconds")
            print(f"Date asked: {question[4]}")
            print(f"Times asked: {question[3]+1}")

        print("--------------------------------------------------")
        print()

        increase_count_of_question(conn, cur, m)

def details(cur, m):
    print()

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
            usage("dd")
            return

        print(f"Here is the conversations with the given date [{m}]")
        conversations=select_conversations_give_date(cur, m)

    print()

    print("--------------------------------------------------")
    print()

    if len(conversations)==0:
        if m.isnumeric():
            print(f"No Conversation with id [{m}]")
        else:
            print("No Conversations to show!")
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

def usage(m):
    if m=="h":
        print()
        print("Usage: [options]")
        print()
        print("Options:")
        print("    h,    help: display this message")
        print("         clear: clear the console")
        print("          exit: exit OpenAIConnector")
        print()
        print("       chatgpt: ask chatgpt a question")
        print("       details: view details about existing conversations")
        print()
    elif m=="o":
        print()
        print("Usage: chatgpt [question]")
        print()
    elif m=="d":
        print()
        print("Usage: details [options]")
        print()
        print("Options:")
        print("    t,       today: display a report for today's conversations")
        print("    y,   yesterday: display a report for yesterday's conversations")
        print("    a,         all: display a report for all conversations")
        print("    m,        most: display a report for the most asked conversation")
        print("    l,     longest: display a report for the conversation that took the longest")
        print("    s,    shortest: display a report for the conversation that took the shortest")
        print("              [id]: display the report for the conversation with the given id")
        print("       date [date]: display the report for the conversation with the given date")
        print("                     (expected format: YYYY-MM-DD)")
        print()
    elif m=="dd":
        print("Usage: details date [YYYY-DD-MM]")
        print()

def openai_proc():
    os.system("clear")

    print("------------------------------------------------")
    print("|         Welcome to OpenAIConnector           |")
    print("|                                              |")
    print("|   I was created to help you connect with     |")
    print("|   ChatGPT and provide insightful analytics   |")
    print("|   about your conversations with ChatGPT!     |")
    print("|                                              |")
    print("|   To ask ChatGPT a question simply type:     |")
    print("|       chatgpt                                |")
    print("|                                              |")
    print("|   To view a detailed report type:            |")
    print("|       details                                |")
    print("|                                              |")
    print("|   To ask for help type:                      |")
    print("|       help or h                              |")
    print("|                                              |")
    print("------------------------------------------------")
    print()

    conn, cur = create_connection()

    create_table(conn, cur)

    while True:
        messages = str(input("oaic$ "))

        if messages.find("exit")!=-1:break

        if messages.find("&&")!=-1:messages=messages.split("&&")
        else:messages=messages.split(";")

        for message in messages:
            message=message.strip()
            if message=="help" or message=="h" : usage("h")
            elif message=="clear": os.system("clear")
            elif message=="": pass
            elif message.find("chatgpt")==0:
                if message=="chatgpt":usage("o")
                else: chatgpt(
                    conn, cur,
                    message.replace("chatgpt ", "").replace("\'", "\"").lower().strip()
                )
            elif message.find("details")==0:
                if message=="details": usage("d")
                else:
                    d=message.replace("details ", "")

                    if d=="t" or d=="today" or \
                       d=="y" or d=="yesterday" or \
                       d=="a" or d=="all" or \
                       d=="m" or d=="most" or \
                       d=="l" or d=="longest" or \
                       d=="s" or d=="shortest" or \
                       d.isnumeric() or \
                       d.find("date") == 0 : details(cur, d)
                    else: usage("d")
            else: print(f"oaic: command not found: {message}")

    print("exit")
    cur.close()
    conn.close()

openai_proc()