import json
from flask import Flask, render_template, request, redirect, url_for
from database_handler_mock import DataBaseHandlerMock
from databaste_handler import DataBaseHandler

app = Flask(__name__)
db_handler: DataBaseHandler = DataBaseHandler()

def get_quiz_data(json_file: str) -> dict:
    with open(json_file, encoding="utf-8") as json_file:
        quiz_data: dict = json.load(json_file)
    return quiz_data

quiz_data = get_quiz_data("quiz_data.json")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_submit', methods=['POST'])
def login_submit():
    user_name: str | None = request.form.get("user_name")
    if user_name is None:
        return redirect(url_for('login'))

    db_handler.set_user(user_name=user_name)
    return redirect(url_for('quiz', user_name=user_name))

@app.route('/quiz')
def quiz():
    user_name: str | None = request.args.get("user_name")
    if user_name is None:
        return redirect(url_for('login'))

    number_of_questions: int = len(quiz_data)
    best_score: float = db_handler.get_best_score(user_name=user_name) / number_of_questions
    return render_template(
        'quiz.html', 
        quiz_data=quiz_data, 
        best_score=round(best_score * 100, 2),
        user_name=user_name
    )

@app.route('/submit', methods=['POST'])
def submit():
    score: int = 0
    number_of_questions: int = len(quiz_data)
    user_name: str | None = request.form.get("user_name")
    if user_name is None:
        return redirect(url_for('login'))
    
    for question in quiz_data:
        question_id: int = question["id"]
        selected_option: str = request.form.get(f"question-{question_id}")
        if selected_option == question["answer"]:
            score += 1
    db_handler.update_best_score(
        user_name=user_name,
        score=score
    )
    best_score: float = db_handler.get_best_score(user_name=user_name) / number_of_questions
    return render_template(
        'result.html', 
        score=score, 
        total_questions=number_of_questions,
        best_score=round(best_score * 100, 2),
        user_name=user_name
    )

if __name__ == '__main__':
    app.run(debug=True)
