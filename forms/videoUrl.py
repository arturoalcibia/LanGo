import re
import requests

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

import youtube

def validate_url(inForm, inField):
    '''
    '''
    urlStr = inField.data

    videoId = youtube.getVideoId(urlStr)

    if not videoId:
        raise ValidationError('Url does not seem to be a valid youtube video url.')

    videoBasicInfo = youtube.getVideoBasicInfo(videoId)

    # Match if video is available/ not private/ exists.
    if not videoBasicInfo:
        raise ValidationError('Youtube video url can\'t be accesed, maybe it\'s private?.')

    # todo! too broad!
    videoInfo = youtube.getVideoInfo(videoId)

    if not videoInfo:
        raise ValidationError('Youtube video does not have any subtitles.')

    inForm.VIDEO_ID = videoId

class VideoUrlForm(FlaskForm):
    url = StringField('Username', validators=[DataRequired(), validate_url])
    search = SubmitField('Search')

    VIDEO_ID = None

