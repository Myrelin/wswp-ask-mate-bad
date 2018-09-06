import connection
from datetime import datetime
import hash
import psycopg2


@connection.connection_handler
def add_question(cursor, question):
    question['submission_time'] = datetime.now()
    question['vote_number'] = 0
    question['view_number'] = 0
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, user_id) 
        VALUES(%s, %s, %s, %s, %s, %s)""", (
        question['submission_time'], question['view_number'], question['vote_number'], question['title'],
        question['message'], question['user_id']))
    cursor.execute("SELECT * FROM question")
    result = cursor.fetchall()
    return result


@connection.connection_handler
def display_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id DESC
                    LIMIT 5;
    """)
    latest_questions = cursor.fetchall()
    return latest_questions


@connection.connection_handler
def add_answer(cursor, answer):
    answer['submission_time'] = datetime.now()
    answer['vote_number'] = 0
    cursor.execute("""INSERT INTO answer (submission_time, vote_number, question_id, message, user_id) 
    VALUES (%s, %s, %s, %s, %s)""", (
        answer['submission_time'], answer['vote_number'], answer['question_id'], answer['message'], answer['user_id']))
    cursor.execute("SELECT * FROM answer")
    result = cursor.fetchall()
    return result


@connection.connection_handler
def search(cursor, search_term):
    cursor.execute("""SELECT title, id FROM question 
    WHERE to_tsvector('english', title) @@ to_tsquery('english', '%{}%');
    """.format(search_term))
    search_result = cursor.fetchall()
    return search_result


@connection.connection_handler
def get_all_question(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                    """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def data_sort_by_atr(cursor, atr, ascend):
    if ascend:
        cursor.execute(
            """
            SELECT * FROM question
            ORDER BY {} DESC
            """.format(atr)
        )
    else:
        cursor.execute(
            """
            SELECT * FROM question
            ORDER BY {} ASC 
            """.format(atr)
        )
    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                    """)
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title,
                    question.message, question.user_id, users.username, users.reputation
                    FROM question
                    INNER JOIN users ON question.user_id = users.id
                    WHERE question.id={};
                    """.format(question_id))
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer WHERE id={};
                    """.format(id))
    answer = cursor.fetchall()
    return answer


@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT answer.id, answer.submission_time, answer.vote_number, answer.question_id ,answer.accepted,
                     answer.message, answer.user_id, users.username, users.reputation FROM answer 
                     INNER JOIN users ON answer.user_id = users.id
                    WHERE answer.question_id={}
                    ORDER BY id ASC;
                    """.format(question_id))
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def delete_questions(cursor, question_id):
    cursor.execute("""
                        DELETE FROM answer
                        WHERE question_id = {};
                        """.format(question_id))
    cursor.execute("""
                        DELETE FROM question
                        WHERE id = {};
                        """.format(question_id))


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                        DELETE FROM answer
                        WHERE id = {};
                        """.format(answer_id))


@connection.connection_handler
def increase_view_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number+1
                    WHERE id={};
                    """.format(question_id))


@connection.connection_handler
def get_user_id_question(cursor, question_id):
    cursor.execute("""SELECT user_id FROM question
                    WHERE question.id = {};""".format(question_id))
    result = cursor.fetchone()
    return result


@connection.connection_handler
def get_user_id_answer(cursor, id):
    cursor.execute("""SELECT user_id FROM answer
                    WHERE answer.id = {};""".format(id))
    result = cursor.fetchone()
    return result

@connection.connection_handler
def voting(cursor, id, question, direction, reputation_id):
    if question:
        if direction == 'up':
            cursor.execute(
                """
                UPDATE question SET vote_number = vote_number + 1
                WHERE id = {};
                """.format(id)
            )
            cursor.execute(""" UPDATE users 
            SET reputation = reputation + 5
            FROM question
            WHERE users.id  = %(uid)s;
            """, {"uid": reputation_id['user_id']})

        else:
            cursor.execute(
                """
                UPDATE question SET vote_number = vote_number - 1
                WHERE id = {};
                """.format(id)
            )
            cursor.execute(""" 
            UPDATE users 
            SET reputation = reputation - 2
            FROM question
            WHERE users.id = %(uid)s ;
                        """, {"uid": reputation_id['user_id']})
    else:
        if direction == 'up':
            cursor.execute(
                """
                UPDATE answer SET vote_number = vote_number + 1
                WHERE id = {};
                """.format(id)
            )
            cursor.execute(""" UPDATE users 
                               SET reputation = reputation + 10
                               FROM answer
                               WHERE users.id = %(uid)s;
                        """, {"uid": reputation_id['user_id']}
                           )
        else:
            cursor.execute(
                """
                UPDATE answer SET vote_number = vote_number - 1
                WHERE id = {};
                """.format(id)
            )
            cursor.execute(""" UPDATE users 
                               SET reputation = reputation - 2
                               FROM  answer
                               WHERE users.id = %(uid)s ;
                        """, {"uid": reputation_id['user_id']}
                           )


@connection.connection_handler
def update_answer(cursor, answer):
    cursor.execute(
        """
        UPDATE answer
        SET message = '{}' 
        WHERE id = {};
        """.format(answer['message'], answer['id'])
    )


@connection.connection_handler
def setup_database(cursor):
    cursor.execute(
        """
            CREATE TABLE users (
        ID SERIAL PRIMARY KEY,
        username varchar(255) NOT NULL UNIQUE,
        pw_hash varchar(255),
        creation_date DATE,
        reputation INT DEFAULT 0
        );
        ALTER TABLE question
        ADD COLUMN user_id INT;
        ALTER TABLE answer 
        ADD COLUMN user_id INT;
        """
    )


@connection.connection_handler
def list_users(cursor):
    cursor.execute("""
        SELECT id, username, reputation, creation_date
        FROM users
        ORDER BY username ASC;
    """)
    user_list = cursor.fetchall()
    return user_list


@connection.connection_handler
def create_user(cursor, username, password):
    pw_hash = hash.hash_password(password)
    date = datetime.now()
    try:
        cursor.execute(
            """
            INSERT INTO users (username, pw_hash, creation_date)
            VALUES (%s,%s,%s)
            
            """, (username, pw_hash, date)
        )
        return True
    except psycopg2.IntegrityError:
        return False


@connection.connection_handler
def questions_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT users.id, users.username, question.title, question.id AS question_id FROM users 
                    INNER JOIN question
                    ON users.id = question.user_id
                    WHERE users.id = %(uid)s""", {"uid": user_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def answers_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT users.id, users.username, answer.message, answer.id AS answer_id FROM users
                    INNER JOIN answer
                    ON users.id = answer.user_id
                    WHERE users.id = %(uid)s""", {"uid": user_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def check_login(cursor, username, password):
    cursor.execute(
        """
        SELECT username, pw_hash FROM users
        WHERE username = '{}'

        """.format(username)
    )
    data = cursor.fetchone()
    if data is None:
        return False
    if data['username'] == username and hash.verify_password(password, data['pw_hash']):
        return True
    else:
        return False


@connection.connection_handler
def get_user_by_username(cursor, username):
    cursor.execute(
        """
        SELECT id FROM users
        WHERE username = '{}'
        """.format(username)
    )
    data = cursor.fetchone()
    return data['id']

@connection.connection_handler
def add_accepted_col(cursor):
    cursor.execute(
        """
        ALTER TABLE answer
        ADD COLUMN accepted BOOLEAN DEFAULT FALSE NOT NULL 
        """
    )

@connection.connection_handler
def accepting_answer(cursor,id):
    cursor.execute(
        """
        UPDATE answer SET accepted = TRUE 
        WHERE id = %(answer_id)s;
        """, {"answer_id": id}

    )

if __name__ == "__main__":
    # setup_database()
    # create_user("admin","admin")
    add_accepted_col()