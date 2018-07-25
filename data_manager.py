import connection
import time


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
    connection.write_new_answer(record_to_add)


def get_all_question():
    questions = connection.get_all_question()
    questions = sorted(questions, key=lambda x: x['submission_time'], reverse=True)
    return questions


def get_question_by_id(data, question_id):
    for item in data:
        if item['id'] == str(question_id):
            data_question = item
    return data_question


def convert_timestamp(data):
    data['submission_time'] = time.ctime(int(data['submission_time']))
    return data


def get_all_answer(question_id):
    answers = connection.get_all_answer()
    answers_for_question = []
    for item in answers:
        if item['question_id'] == str(question_id):
            item = convert_timestamp(item)
            answers_for_question.append(item)
    return answers_for_question
