from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

import constants

class SearchVideoForm(FlaskForm):
    searchQuery = StringField('Search query',
                              validators=[DataRequired()])
    language = SelectField('language',
                           choices=constants.ISO_LANGUAGE_CODE_MAPPING.keys())
    submit = SubmitField('Search')

