from flask import Flask, render_template, request, redirect, url_for


import data_manager

app = Flask(__name__)



@app.route('/list')
def route_home():
    questions = data_manager.get_all_question()
    return render_template('list.html', questions=questions)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def latest_five_questions():
    latest_questions = data_manager.display_latest_questions()
    return render_template('index.html', latest_questions=latest_questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    data_manager.increase_view_number(question_id)
    data_question = data_manager.get_question_by_id(question_id)
    answers_for_question = data_manager.get_answers_for_question(question_id)
    return render_template('question.html', data_question=data_question, answers_for_question=answers_for_question)

# @app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
# def edit_question(question_id):
#     data_question = data_manager.get_question_by_id(questions, question_id)
    


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
        return redirect('/question/{}'.format(question_id))
    else:
        return render_template('new_answer.html', question_id=question_id)


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_questions(question_id)
    return redirect('/')


@app.route('/list/<atr>/<direction>')
def order_by(atr, direction):
    if direction == 'asc':
        questions = data_manager.data_sort_by_atr(atr, True)
    else:
        questions = data_manager.data_sort_by_atr(atr, False)
    return render_template('list.html', questions=questions)


@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    answers = data_manager.get_all_answers()
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer['question_id']
    data_manager.delete_answer(answer_id)
    return redirect('/question/{}'.format(question_id))


@app.route('/question/<id>/vote/<direction>/<question>')
def vote(id, direction, question):
    if question == 'yes':
        data_manager.voting(id, True, direction)
        return redirect('/question/{}'.format(id))
    else:
        data_manager.voting(id, False, direction)
        answer = data_manager.get_answer_by_id(id)
        return redirect('/question/{}'.format(answer[0]['question_id']))

@app.route('/question/<id>/view_number')
def increase_view_number(id):
    data_manager.increase_view_number(id)
    return redirect('question/{}'.format(id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
