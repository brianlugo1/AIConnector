from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import datetime
import psycopg2
import os

def create_connection():
    conn = psycopg2.connect("dbname=openai")
    cur = conn.cursor()
    return conn, cur

def create_table(conn, cur):
    cur.execute("CREATE TABLE IF NOT EXISTS conversation (id serial PRIMARY KEY, question varchar UNIQUE NOT NULL, answer varchar NOT NULL, count integer NOT NULL, day date NOT NULL);")
    conn.commit()

def delete_table(conn, cur):
    cur.execute("DROP TABLE IF EXISTS conversation;")
    conn.commit()

def clear_table(conn, cur):
    cur.execute("TRUNCATE conversation;")
    conn.commit()

def select_table_names(cur):
    cur.execute("select * from pg_catalog.pg_tables where schemaname='public';")
    return cur.fetchall()

def select_table_columns(cur):
    cur.execute("SELECT * FROM information_schema.columns WHERE table_name='conversation';")
    return cur.fetchall()

def print_table_details(cur):
    print("Details about Table:")
    print()
    print("Name:   ", select_table_names(cur)[0][1])

    for table in select_table_columns(cur):
        print("Column: ", table[3], "( Type: ", table[7], ")")

    print()

def select_all_conversations(cur):
    cur.execute("SELECT * FROM conversation;")
    return cur.fetchall()

def insert_conversation(conn, cur, question, answer):
    cur.execute(f"INSERT INTO conversation (question, answer, count, day) VALUES (\'{question}\', \'{answer}\', 1, \'{datetime.datetime.now().date()}\');")
    conn.commit()

def delete_conversation(conn, cur, question, answer):
    cur.execute(f"DELETE FROM conversation WHERE conversation.question=\'{question}\' AND conversation.answer=\'{answer}\';")
    conn.commit()

def search_question(cur, question):
    cur.execute(f"SELECT * FROM conversation WHERE conversation.question=\'{question}\';")
    return cur.fetchall()

def increase_count_of_question(conn, cur, question):
    cur.execute(f"UPDATE conversation SET count = count+1 WHERE conversation.question=\'{question}\';")
    conn.commit()

def select_questions_asked(cur, d):
    day=""

    if d=="t": day=datetime.datetime.now().date()
    elif d=="y": day=datetime.datetime.now().date().replace(day=datetime.datetime.now().date().day-1)
    elif d=="a": return select_all_conversations(cur)

    cur.execute(f"SELECT * FROM conversation WHERE conversation.day=\'{day}\';")

    return cur.fetchall()

def select_most_asked_question(cur):
    cur.execute(f"SELECT * FROM conversation WHERE count=(SELECT MAX(count) FROM conversation);")
    return cur.fetchall()

def chatgpt(conn, cur, m):
    questions=search_question(cur, m)

    if len(questions)==0:
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

        print()
        print(completion.choices[0].message.content)
        print()

        insert_conversation(conn, cur, m, completion.choices[0].message.content)
    else:
        print()
        print("Question already asked:")
        print()
        for question in questions:
            print("Stored answer: ", question[2])
            print()
            print("Date asked: ", question[4])
            print("Times asked: ", question[3]+1)
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
    
    print()

    if len(conversations)==0:
        print("No Conversations to show!")
        print()

    for conversation in conversations:
        print("Question: ")
        print(conversation[1])
        print()
        print("Answer: ")
        print(conversation[2])
        print()
        print("Date asked: ", conversation[4])
        print("Times asked: ", conversation[3])
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
        print("    t,      today: display a report for today's conversations")
        print("    y,  yesterday: display a report for yesterday's conversations")
        print("    a,        all: display a report for yesterday's conversations")
        print("    m,       most: display a report for the most asked conversation")
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
        message = str(input("oaic$ "))

        if message=="help" or message=="h" : usage("h")
        elif message=="clear": os.system("clear")
        elif message=="exit": break
        elif message=="": pass
        elif message.find("chatgpt")!=-1:
            if message=="chatgpt":usage("o")
            else: chatgpt(conn, cur, message.replace("chatgpt ", "").lower().strip())
        elif message.find("details")!=-1:
            if message=="details": usage("d")
            else:
                d=message.replace("details ", "")
                if d=="t" or d=="today" or d=="y" or d=="yesterday" or d=="a" or d=="all" or d=="m" or d=="most": details(cur, d)
                else: usage("d")
        else: usage("h")

    cur.close()
    conn.close()

openai_proc()