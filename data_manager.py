import connection
from datetime import datetime
import time

DATA_HEADER_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@connection.connection_handler
def add_question(cursor, question):
    cursor.execute("""INSERT INTO question (id, submission_time, vote_number, question_id, message, image) 
        VALUES (%s %s %s %s %s %s )""", (
    question['submission_time'], question['view_number'], question['vote_number'], question['title'], question['message'], question['image']))
    cursor.execute("SELECT * FROM question")
    result = cursor.fetchall()
    return result


@connection.connection_handler
def add_answer(cursor, answer):
    cursor.execute("""INSERT INTO answer (id, submission_time, vote_number, question_id, message, image) 
    VALUES (%s %s %s %s %s )""", (answer['submission_time'], answer['vote_number'], answer['question_id'], answer['message'], answer['image']))
    cursor.execute("SELECT * FROM answer")
    result = cursor.fetchall()
    return result


@connection.connection_handler
def get_all_question(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                    """)
    questions = cursor.fetchall()
    return questions


def data_sort_by_atr(data, atr, ascend):
    try:
        for line in data:
            line[atr] = int(line[atr])
    except ValueError:
        pass
    if ascend:
        data = sorted(data, key=lambda x: x[atr])
    else:
        data = sorted(data, key=lambda x: x[atr], reverse=True)
    for line in data:
        line[atr] = str(line[atr])
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
    cursor.execute(
    "SELECT * FROM question WHERE id=%s", (question_id))
    question = cursor.fetchall()
    return question

@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute(
    "SELECT * FROM question WHERE id=%s", (answer_id))
    answer = cursor.fetchall()



def convert_timestamp(data):
    data['submission_time'] = time.ctime(int(data['submission_time']))
    return data


def get_answers_for_question(question_id):
    answers = connection.get_all_answer()
    answers_for_question = []
    for item in answers:
        if item['question_id'] == str(question_id):
            item = convert_timestamp(item)
            answers_for_question.append(item)
    return answers_for_question


def delete_questions(question_id):
    questions = get_all_question()
    answers = get_all_answers()
    for i in range(len(questions)):
        if questions[i]['id'] == question_id:
            del questions[i]
            break
    answers_for_question = get_answers_for_question(question_id)
    for answer in answers_for_question:
        for i in range(len(answers)):
            if answer['id'] == answers[i]['id']:
                del answers[i]
                break
    connection.write_data(questions, DATA_HEADER_Q)
    connection.write_data(answers, DATA_HEADER_A, False)


def delete_answer(answer_id):
    answers = get_all_answers()
    for i in range(len(answers)):
        if answers[i]['id'] == answer_id:
            del answers[i]
            break
    connection.write_data(answers, DATA_HEADER_A, False)


def increase_view_number(question_id):
    questions = get_all_question()
    for i in range(len(questions)):
        if questions[i]['id'] == question_id:
            questions[i]['view_number'] = int(questions[i]['view_number'])
            questions[i]['view_number'] += 1
            questions[i]['view_number'] = str(questions[i]['view_number'])
            connection.write_data(questions, DATA_HEADER_Q, True)


def voting(id, question, direction):
    if question:
        questions = get_all_question()
        question = get_question_by_id(questions, id)
        if direction == 'up':
            try:
                question['vote_number'] = int(question['vote_number'])
                question['vote_number'] += 1
                question['vote_number'] = str(question['vote_number'])
            except ValueError:
                print('ERROR')
        else:
            try:
                question['vote_number'] = int(question['vote_number'])
                question['vote_number'] -= 1
                question['vote_number'] = str(question['vote_number'])
            except ValueError:
                print('ERROR')
        for i in range(len(questions)):
            if questions[i]['id'] == question['id']:
                questions[i] = question
        connection.write_data(questions, DATA_HEADER_Q, True)
    else:
        answers = get_all_answers()
        answer = get_answer_by_id(answers, id)
        if direction == 'up':
            try:
                answer['vote_number'] = int(answer['vote_number'])
                answer['vote_number'] += 1
                answer['vote_number'] = str(answer['vote_number'])
            except ValueError:
                print('ERROR')
        else:
            try:
                answer['vote_number'] = int(answer['vote_number'])
                answer['vote_number'] -= 1
                answer['vote_number'] = str(answer['vote_number'])
            except ValueError:
                print('ERROR')
        for k in range(len(answers)):
            if answers[k]['id'] == answer['id']:
                answers[k] == answer
        connection.write_data(answers, DATA_HEADER_A, False)
