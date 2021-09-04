import re
import requests

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

import youtube_dl

YOUTUBE_URL_RE = re.compile('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)(?P<code>[\w\-]+)(\S+)?$')

def validate_url(inForm, inField):

    urlStr = inField.data

    # Match if youtube url #
    urlMatch = YOUTUBE_URL_RE.match(urlStr)
    if not urlMatch:
        raise ValidationError('Url does not seem to be a valid youtube video url.')

    videoCode = urlMatch.group('code') # Ex: cAoR6FUE0kk
    requestUrl = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={0}'.format(
        videoCode)
    requestObj = requests.get(url=requestUrl)

    # Match if video is available/ not private/ exists.
    if not requestObj.status_code != '200':
        raise ValidationError('Youtube video url can\'t be accesed, maybe it\'s private?.')

    with youtube_dl.YoutubeDL({}) as ydl:
        videoInfo = ydl.extract_info(urlStr, download=False)

    subtitles = videoInfo.get('subtitles', {})

    if not subtitles:
        raise ValidationError('Youtube video does not have any subtitles.')

    # Store extra info #
    inForm.videoTitle = videoInfo['title']
    print('#' * 80 )
    print(list(subtitles.keys()))
    inForm.subtitles  = list(subtitles.keys()) or []

class VideoUrlForm(FlaskForm):
    url = StringField('Username', validators=[DataRequired(), validate_url])
    submit = SubmitField('Next')

