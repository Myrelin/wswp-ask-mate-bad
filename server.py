from flask import Flask


app = Flask(__name__)


@app.route('/')
@app.route('/list')


@app.route('/question/<question_id>')


@app.route('/add_question')




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
