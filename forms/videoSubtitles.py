from flask_wtf import FlaskForm
from wtforms import SelectField

class VideoSubtitlesForm(FlaskForm):
    subtitles = SelectField(u"Filename")
