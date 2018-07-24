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
            data_question = item
    data_question['submission_time'] = time.ctime(int(data_question['submission_time']))

    answers = connection.get_all_answer()
    answers_for_question = []
    for item in answers:
        if item['question_id'] == str(question_id):
            item['submission_time'] = time.ctime(int(item['submission_time']))
            answers_for_question.append(item)
    return render_template('question.html', data_question=data_question, answers_for_question=answers_for_question)


@app.route('/add_question')
def add_question():
    return redirect('/')



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
