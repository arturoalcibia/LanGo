from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, AnyOf

import constants

languageNames = list(constants.LANGUAGE_ISO_CODE_MAPPING.keys())
languageNames.append('')

class SearchVideoForm(FlaskForm):

    searchQuery = StringField('Search query',
                              validators=[DataRequired()])
    language = StringField('language',
                           validators=[AnyOf(languageNames)])
    submit = SubmitField('Search')

