from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField

class ExerciseSettingsForm(FlaskForm):
    nextBtn = SubmitField('Start Exercise')

