from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_home():
    questions = data_manager.get_all_question()
    questions = sorted(questions, key=lambda x: x['submission_time'], reverse=True)
    # @app.route('/question/<question_id>')

    # @app.route('/add_question')
    return render_template('list.html', questions=questions)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
