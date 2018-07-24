import os
import csv

QUESTION_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_question():
    with open(QUESTION_DATA_FILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        all_question = list(reader)
        return all_question


def get_all_answer():
    with open(ANSWER_DATA_FILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        all_answer = list(reader)
        return all_answer


def write_new_answer(data):
    with open(QUESTION_DATA_FILE_PATH, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writerow(data)
