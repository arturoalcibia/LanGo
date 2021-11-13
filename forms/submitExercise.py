from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

class SubmitExerciseForm(FlaskForm):
    currentScore = IntegerField('Current Score:', validators=[DataRequired()])
    submit = SubmitField('Search')