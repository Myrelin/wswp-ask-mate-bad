import os
import csv

QUESTION_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'


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


def write_new_answer(data, DATA_HEADER, question=True):
    if question:
        with open(QUESTION_DATA_FILE_PATH, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
            writer.writerow(data)
    else:
        with open(ANSWER_DATA_FILE_PATH, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
            writer.writerow(data)

def write_data(data, DATA_HEADER, question=True):
    if question:
        with open(QUESTION_DATA_FILE_PATH, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
            writer.writeheader()
            for line in data:
                writer.writerow(line)
    else:
        with open(ANSWER_DATA_FILE_PATH, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
            writer.writeheader()
            for line in data:
                writer.writerow(line)