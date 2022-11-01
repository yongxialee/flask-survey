from flask import Flask, request, render_template,flash,session, redirect
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey
#key names will use to store client's data in the session;
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "ThisHappy12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_survey_start():
    """start survey by choosing a survey form"""
    return render_template('start.html', survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")
    
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)
    print(responses)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # access invalid question.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)
@app.route('/answer', methods=["POST"])
def handle_question():
    
    answer=request.form['answer']
    #add answer to seesion
    responses=session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    
    if (len(responses)==len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")
@app.route('/complete')
def complte():
    return render_template('complete.html',survey=survey)
        
        
