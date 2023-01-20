from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key93'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def show_survey():
    '''Start the survey'''
    return render_template('start.html', survey=survey)


@app.route('/questions/<int:q>')
def show_question(q):
    '''Display question'''
    if (responses is None):
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    if (len(responses) != q):
        flash(f"Invalid question id: {q}")
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[q]

    return render_template('questions.html', question=question)


@app.route('/answer', methods=['POST'])
def handle_answer():
    '''Add response to the list and redirect to the next question'''
    answer = request.form['answer']
    responses.append(answer)

    if(len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/complete')
def complete():
    '''Survey completed'''
    return render_template('completion.html')
