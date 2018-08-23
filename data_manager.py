import connection
from datetime import datetime

DATA_HEADER_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@connection.connection_handler
def add_question(cursor, question):
    question['submission_time'] = datetime.now()
    question['vote_number'] = 0
    question['view_number'] = 0
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
        VALUES(%s, %s, %s, %s, %s, %s)""", (question['submission_time'], question['view_number'], question['vote_number'], question['title'], question['message'], question['image']))
    cursor.execute("SELECT * FROM question")
    result = cursor.fetchall()
    return result

@connection.connection_handler
def display_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id DESC
                    LIMIT 5;
    """)
    latest_questions = cursor.fetchall()
    return latest_questions


@connection.connection_handler
def add_answer(cursor, answer):
    answer['submission_time'] = datetime.now()
    answer['vote_number'] = 0
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
    VALUES (%s, %s, %s, %s, %s)""", (answer['submission_time'], answer['vote_number'], answer['question_id'], answer['message'], answer['image']))
    cursor.execute("SELECT * FROM answer")
    result = cursor.fetchall()
    return result

@connection.connection_handler
def search(cursor, search_term):
    cursor.execute("""SELECT title, id FROM question 
    WHERE to_tsvector('english', title) @@ to_tsquery('english', '%{}%');
    """.format(search_term))
    search_result = cursor.fetchall()
    # for result in search_result:
    #     result['title'] = result['title'].replace(search_term['query'])
    #     result['message'] = result['message'].replace(search_term['query'])
    return search_result

@connection.connection_handler
def get_all_question(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def data_sort_by_atr(cursor, atr, ascend):
    if ascend:
        cursor.execute(
            """
            SELECT * FROM question
            ORDER BY {} DESC
            """.format(atr)
        )
    else:
        cursor.execute(
            """
            SELECT * FROM question
            ORDER BY {} ASC 
            """.format(atr)
        )
    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                    """)
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question WHERE id={};
                    """.format(question_id))
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer WHERE id={};
                    """.format(id))
    answer = cursor.fetchall()
    return answer



@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer 
                    WHERE question_id={}
                    ORDER BY id ASC;
                    """.format(question_id))
    answers = cursor.fetchall()
    return answers

@connection.connection_handler
def delete_questions(cursor, question_id):
    cursor.execute("""
                        DELETE FROM question
                        WHERE id = {};
                        """.format(question_id))
    cursor.execute("""
                        DELETE FROM answer
                        WHERE question_id = {};
                        """.format(question_id))

@connection.connection_handler
def delete_answer(cursor,answer_id):
    cursor.execute("""
                        DELETE FROM answer
                        WHERE id = {};
                        """.format(answer_id))


@connection.connection_handler
def increase_view_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number+1
                    WHERE id={};
                    """.format(question_id))



@connection.connection_handler
def voting(cursor, id, question, direction,):
    if question:
        if direction == 'up':
            cursor.execute(
                """
                UPDATE question SET vote_number = vote_number + 1
                WHERE id = {};
                """.format(id)
            )
        else:
            cursor.execute(
                """
                UPDATE question SET vote_number = vote_number - 1
                WHERE id = {};
                """.format(id)
            )
    else:
        if direction == 'up':
            cursor.execute(
                """
                UPDATE answer SET vote_number = vote_number + 1
                WHERE id = {};
                """.format(id)
            )
        else:
            cursor.execute(
                """
                UPDATE answer SET vote_number = vote_number - 1
                WHERE id = {};
                """.format(id)
            )


@connection.connection_handler
def update_answer(cursor,answer):
    cursor.execute(
        """
        UPDATE answer
        SET message = '{}', image ='{}' 
        WHERE id = {}
        """.format(answer['message'], answer['image'], answer['id'])
    )


