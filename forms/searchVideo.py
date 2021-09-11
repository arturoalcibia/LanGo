from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, AnyOf

import constants

class SearchVideoForm(FlaskForm):
    languageNames = list(constants.LANGUAGE_ISO_CODE_MAPPING.keys())
    languageNames.append('')

    searchQuery = StringField('Search query',
                              validators=[DataRequired()])
    language = StringField('language',
                           validators=[AnyOf(languageNames)])
    submit = SubmitField('Search')

