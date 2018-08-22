import connection
import time

DATA_HEADER_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def add_question(data):
    questions = connection.get_all_question()
    try:
        new_id = str(int(questions[-1]['id']) + 1)
    except IndexError:
        new_id = '1'
    record_to_add = data
    record_to_add['id'] = new_id
    record_to_add['submission_time'] = str(int(round(time.time())))
    record_to_add['view_number'] = '0'
    record_to_add['vote_number'] = '0'
    connection.write_new_answer(record_to_add, DATA_HEADER_Q)


def add_answer(data):
    answers = connection.get_all_answer()
    try:
        new_id = str(int(answers[-1]['id']) + 1)
    except IndexError:
        new_id = '1'
    record_to_add = data
    record_to_add['id'] = new_id
    record_to_add['submission_time'] = str(int(round(time.time())))
    record_to_add['vote_number'] = '0'
    record_to_add['question_id'] = data['question_id']
    connection.write_new_answer(record_to_add, DATA_HEADER_A, False)


@connection.connection_handler
def get_all_question(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def data_sort_by_atr(atr, ascend, cursor):
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
    answers = cursor.execute("""
                    SELECT * FROM answer;
                    """)
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question WHERE id=%s;
                    """, question_id)
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM question WHERE id=%s;
                    """, answer_id)
    answer = cursor.fetchall()
    return answer


def convert_timestamp(data):
    data['submission_time'] = time.ctime(int(data['submission_time']))
    return data


@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer WHERE id={};
                    """.format(question_id))
    answers = cursor.fetchall()
    return answers


def delete_questions(cursor, question_id):

    cursor.execute("""
                        DELETE FROM questions
                        WHERE id = {};
                        """.format(question_id))
    cursor.execute("""
                        DELETE FROM answers
                        WHERE question_id = {};
                        """.format(question_id))
    # questions = get_all_question()
    # answers = get_all_answers()
    # answers_for_question = get_answers_for_question(question_id)
    # for answer in answers_for_question:
    #     for i in range(len(answers)):
    #         if answer['id'] == answers[i]['id']:
    #             del answers[i]
    #             break
    # for i in range(len(questions)):
    #     if questions[i]['id'] == question_id:
    #         del questions[i]
    #         break
    # connection.write_data(questions, DATA_HEADER_Q)
    # connection.write_data(answers, DATA_HEADER_A, False)


def delete_answer(answer_id)

    cursor.execute("""
                        DELETE FROM answers
                        WHERE id = %d;
                        """(answer_id))

    # answers = get_all_answers()
    # for i in range(len(answers)):
    #     if answers[i]['id'] == answer_id:
    #         del answers[i]
    #         break
    # connection.write_data(answers, DATA_HEADER_A, False)

@connection.connection_handler
def increase_view_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number+1
                    WHERE id={};
                    """.format(question_id))



@connection.connection_handler
def voting(id, question, direction,cursor):
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
                UPDATE answer SET vote_number + vote_number - 1
                WHERE id = {};
                """.format(id)
            )

def edit_question(question_id, data_question):
    all_questions = connection.get_all_question()
    for i in range(len(all_questions)):
        if all_questions[i]['id'] == data_question['id']:
            del all_questions[i]
            all_questions.insert(i, edited_question)


