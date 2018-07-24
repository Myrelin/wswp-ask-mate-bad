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
