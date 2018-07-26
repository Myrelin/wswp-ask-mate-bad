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


def get_all_question():
    questions = connection.get_all_question()
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


def get_all_answers():
    answers = connection.get_all_answer()
    return answers


def get_question_by_id(data, question_id):
    for item in data:
        if item['id'] == str(question_id):
            data_question = item
    return data_question


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
    for k in range(len(answers)):
        if answers[k]['question_id'] == question_id:
            del answers[k]
    connection.write_data(questions, DATA_HEADER_Q)
    connection.write_data(answers, DATA_HEADER_A, False)


def delete_answer(answer_id):
    answers = get_all_answers()
    for i in range(len(answers)):
        if answers[i]['id'] == answer_id:
            del answers[i]
    connection.write_data(answers, DATA_HEADER_A, False)
