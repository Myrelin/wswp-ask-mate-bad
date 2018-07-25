from flask import Flask, render_template, request, redirect, url_for


import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_home():
    questions = data_manager.get_all_question()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    questions = data_manager.get_all_question()
    data_question = data_manager.get_question_by_id(questions, question_id)
    data_question = data_manager.convert_timestamp(data_question)
    answers_for_question = data_manager.get_answers_for_question(question_id)
    return render_template('question.html', data_question=data_question, answers_for_question=answers_for_question)


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    page_title = "Ask a QUESTION"
    if request.method == 'POST':
        data = request.form.to_dict()
        data_manager.add_question(data)
        return redirect('/')
    else:
        return render_template('form.html', page_title=page_title)


@app.route('/question/<question_id>/new_answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        data_manager.add_answer(data)
        return redirect('/')
    else:
        return render_template('new_answer.html', question_id=question_id)

@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_questions(request.form['question_id'])
    return redirect('/')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
