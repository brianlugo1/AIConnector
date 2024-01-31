import psycopg2
import datetime



def create_connection():
    conn = psycopg2.connect("dbname=ai")

    cur = conn.cursor()

    return conn, cur


def create_table(conn, cur):
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


def insert_conversation(conn, cur, question, answer, seconds, ai):
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


def delete_conversation(conn, cur, question, answer):
    cur.execute(f"DELETE FROM conversation \
        WHERE conversation.question=E\'{question}\' \
        AND conversation.answer=E\'{answer}\';\
    ")

    conn.commit()


def search_question(cur, question, ai):
    cur.execute(f"SELECT * FROM conversation \
        WHERE conversation.question=E\'{question}\' \
        AND conversation.ai=\'{ai}\';\
    ")

    return cur.fetchall()


def increase_count_of_question(conn, cur, question, ai):
    cur.execute(f"UPDATE conversation \
        SET count = count+1 \
        WHERE conversation.question=E\'{question}\' \
        AND ai=\'{ai}\';\
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

