from flask import Flask, render_template, request, redirect, url_for

import connection
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_home():
    questions = connection.get_all_question()
    questions = sorted(questions, key=lambda x: x['submission_time'], reverse=True)
    return render_template('list.html', questions=questions)

@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    questions = connection.get_all_question()
    for item in questions:
        if item['id'] == str(question_id):
            details = item
    data_question = {'id': details['id'], 'submission_time':time.ctime(int(details['submission_time'])),'view_number':details['view_number'],
            'vote_number':details['vote_number'],'title':details['title'],'message':details['message'],
            'image':details['image']}
    return render_template('question.html', data_question=data_question)

@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_answer(question_id):
    answers = connection.get_all_answer()
    answers_for_question = []
    for item in answers:
        if item['question_id'] == str(question_id):
            answers_for_question.append(item)
    return render_template('question.html', answers_for_question=answers_for_question)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
