from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def root_route():
    """Select survey"""

    return render_template("survey.html", survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    """Reset responses"""

    responses = []

    return redirect('/questions/0')

@app.route('/questions/<int:id>')
def show_question(id):
    """Show passed questions"""
    
    question = survey.questions[id]

    return render_template("question.html", question_num=id, question=question)

@app.route('/answer', methods=['POST'])
def answer_question():
    """Save answer and load next question"""
    choice = request.form['answer']

    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def complete():
    """Survey complete"""

    return render_template('complete.html')