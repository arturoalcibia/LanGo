from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import EqualTo

class BlankExerciseForm(FlaskForm):

    answerStr = ''
    #answerField = StringField('Answer', validators=[EqualTo(answerStr)])
    progress = IntegerField()
    next = SubmitField('Next!')
