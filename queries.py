import psycopg2
import datetime
from Constants import *
from typing import Tuple



def create_connection() -> Tuple | Tuple[None, None]:
    """
    create_connection() attempts to create
    a connection to the postgresql server
    with the db name of ai. Returns the
    connection and cursor on success.
    Returns None otherwise.

    Paramters:
    None

    Returns:
    A Tuple of
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Or A Tuple of
    None
    None
    """
    try:
        conn=psycopg2.connect("dbname=ai")

        cur=conn.cursor()

        return conn, cur

    except:
        return None, None


def create_table(conn, cur) -> None:
    """
    create_table() attempts to create the
    table `conversation` with 7 attributes.
    Once created, create_table() commits
    the changes to the db `ai`.

    Paramters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    None
    """
    cur.execute("CREATE TABLE IF NOT EXISTS conversation (\
        id serial PRIMARY KEY, \
        question varchar NOT NULL, \
        answer varchar NOT NULL, \
        count integer NOT NULL, \
        day date NOT NULL, \
        duration real NOT NULL, \
        ai varchar NOT NULL \
    );")

    conn.commit()


def delete_table(conn, cur) -> None:
    """
    delete_table() attempts to delete the
    table `conversation` if it exists.
    Once deleted, delete_table() commits
    the changes to the db `ai`.

    Paramters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    None
    """
    cur.execute("DROP TABLE IF EXISTS conversation;")

    conn.commit()


def clear_table(conn, cur) -> None:
    """
    clear_table() attempts to clear all
    of the rows in the table `conversation`.
    Once cleared, clear_table() commits
    the changes to the db `ai`.

    Paramters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    None
    """
    cur.execute("TRUNCATE conversation;")

    conn.commit()


def select_table_names(cur) -> list:
    """
    select_table_names() attempts to query
    all of the tables names in the db `ai`.
    Once queried, select_table_names()
    returns the result set of table names.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute("SELECT * FROM pg_catalog.pg_tables \
        WHERE schemaname='public';\
    ")

    return cur.fetchall()


def select_table_columns(cur) -> list:
    """
    select_table_columns() attemps to
    query all of the columns names in
    the table `conversation`. Once
    quieried, select_table_columns()
    returns the result set of table columns.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute("SELECT * FROM information_schema.columns \
        WHERE table_name='conversation';\
    ")

    return cur.fetchall()


def print_table_details(cur) -> None:
    """
    print_table_details() attempts to
    print all of the table names and
    corresponding table columns in
    the db `ai` with details about
    the type.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    None
    """
    print("Details about Table:\n")

    print("Name:   ", select_table_names(cur)[0][1])

    for table in select_table_columns(cur):
        print("Column: ", table[3], "( Type: ", table[7], ")")

    print()


def select_all_conversations(cur) -> list:
    """
    select_all_conversations() attempts
    to query all of the stored conversations
    in the table `conversation`. Once queried,
    select_all_conversations() returns the
    result set of all stored conversations.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute("\
        SELECT * FROM conversation;\
    ")

    return cur.fetchall()


def insert_conversation(conn, cur, question: str, answer: str, seconds: int, ai: str) -> None:
    """
    insert_conversation() attempts to insert
    into the table `conversation` the given
    strings of question, answer, ai, and
    integer seconds. Once inserted,
    insert_conversation() commits the
    changes to the db `ai`.

    Paramters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)
    question: string (The prompt message)
    answer: string (The response from target ai)
    seconds: integer (The seconds target ai responded)
    ai: string (The target ai)

    Returns:
    None
    """
    cur.execute(f"INSERT INTO conversation (\
            question, answer, count, \
            day, duration, ai\
        ) VALUES (\
            E\'{question}\', E\'{answer}\', 1, \
            \'{datetime.datetime.now().date()}\', \
            {seconds}, \'{ai}\'\
        );\
    ")

    conn.commit()


def delete_conversation(conn, cur, question: str, answer: str) -> None:
    """
    delete_conversation() attempts to delete
    the conversation with the given question
    and answer. Once deleted,
    delete_conversation() commits the changes
    to the db `ai`.

    Paramters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)
    question: string (The prompt message)
    answer: string (The response from target ai)

    Returns:
    None
    """
    cur.execute(f"DELETE FROM conversation \
        WHERE conversation.question=E\'{question}\' \
        AND conversation.answer=E\'{answer}\';\
    ")

    conn.commit()


def search_question(cur, question: str, ai: str) -> list:
    """
    search_question() attempts to query
    the conversations with the given
    question and answer. Once queried,
    search_question() returns the result
    set of the matching conversations.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)
    question: string (The prompt message)
    ai: string (The target ai)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute(f"SELECT * FROM conversation \
        WHERE conversation.question=E\'{question}\' \
        AND conversation.ai=\'{ai}\';\
    ")

    return cur.fetchall()


def increase_count_of_question(conn, cur, question: str, ai: str) -> None:
    """
    increase_count_of_question() attempts to
    query the stored conversation that contains
    the given question and target ai and increments
    the times asked by 1. Once queried,
    increase_count_of_question() commits the changes
    to the db `ai`.

    Paramters:
    conn: connection (The connection object returned from `psycopg2.connect()`)
    cur: cursor (The cursor object returned from `conn.cursor()`)
    question: string (The prompt message)
    ai: string (The target ai)

    Returns:
    None
    """
    cur.execute(f"UPDATE conversation \
        SET count=count+1 \
        WHERE conversation.question=E\'{question}\' \
        AND ai=\'{ai}\';\
    ")

    conn.commit()


def select_questions_asked(cur, d: str) -> list:
    """
    select_questions_asked() attempts to query
    the stored conversations given the parsed
    flag. Once queried, select_questions_asked()
    commits the changes to the db `ai`.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)
    d: string (The given flag to filter stored conversations)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    day=""

    if d==TDY[0]:
        day=datetime.datetime.now().date()

    elif d==YTD[0]:
        day=datetime.datetime.now().date().replace(
            day=datetime.datetime.now().date().day-1
        )

    elif d==ALL[0]:
        return select_all_conversations(cur)

    cur.execute(f"SELECT * FROM conversation \
        WHERE conversation.day=\'{day}\';\
    ")

    return cur.fetchall()


def select_most_asked_question(cur) -> list:
    """
    select_most_asked_question() attempts to
    query the conversations with the highest
    times asked. Once queried,
    select_most_asked_questions() returns
    the result set of the conversations with
    the most times asked.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute(f"""
        SELECT * FROM conversation
        WHERE count=(
            SELECT MAX(count)
            FROM conversation
        );
    """)

    return cur.fetchall()


def select_longest_question_waited_for(cur) -> list:
    """
    select_longest_question_waited_for() attempts to
    query the conversation with the longest duration
    of time waited for a target ai to respond. Once
    queried, select_longest_question_waited_for()
    returns the result of the conversations with the
    most asked times.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute(f"SELECT * FROM conversation \
        WHERE duration=(\
            SELECT MAX(duration) \
            FROM conversation\
        );\
    ")

    return cur.fetchall()


def select_shortest_question_waited_for(cur) -> list:
    """
    select_shortest_question_waited_for() attempts to
    query the conversation with the shortest duration
    of time waited for a target ai to respond. Once
    queried, select_shortest_question_waited_for()
    returns the result of the conversation with the
    shortest duration.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute(f"SELECT * FROM conversation \
        WHERE duration=(\
        SELECT MIN(duration) FROM conversation\
    );")

    return cur.fetchall()


def select_conversation_given_id(cur, id: int) -> list:
    """
    select_conversation_given_id() attempts to query
    the conversation with the given id. Once queried,
    select_conversation_given_id() returns the result
    set of the conversation with the given id.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)
    id: integer (The id of a stored conversation)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute(f"SELECT * FROM conversation \
        WHERE id={id};\
    ")

    return cur.fetchall()


def select_conversations_given_date(cur, date: str) -> list:
    """
    select_conversations_given_date() attempts to query
    the conversations with the given date. Once queried,
    select_conversations_given_date() returns the result
    set of the conversations with the given date.

    Paramters:
    cur: cursor (The cursor object returned from `conn.cursor()`)
    date: string (A date to query all stored conversations)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute(f"SELECT * FROM conversation \
        WHERE day=\'{date}\';\
    ")

    return cur.fetchall()


def select_conversations_given_ai(cur, ai: str) -> list:
    """
    select_conversations_given_ai() attempts to query
    the conversations with the given ai. Once queried,
    select_conversations_given_ai() returns the result
    set of the conversations with the given ai.

    Parameters:
    cur: cursor (The cursor object returned from `conn.cursor()`)
    ai: string (The target ai)

    Returns:
    cur.fetchall(): list (The list of table names in the db `ai`)
    """
    cur.execute(f"SELECT * FROM conversation \
        WHERE ai=\'{ai}\';\
    ")

    return cur.fetchall()