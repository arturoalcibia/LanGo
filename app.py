import urllib.request
import xml.etree.ElementTree

from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request

import constants
from forms.searchVideo import SearchVideoForm
from forms.exercise import BlankExerciseForm
from forms.exerciseSettings import ExerciseSettingsForm

import youtube

DEBUG = True
SECRET_KEY = "secret"

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
@app.route("/index")
def index():
    '''Index page, Let's you sign up/ log in or continue as guest.
    Gets redirected if a session exists.
    '''
    #todo!
    # If signed skip to next page

    return render_template("index.html")

@app.route('/browse/<query>/<language>', methods=("GET", "POST"))
@app.route('/browse/<query>/', methods=("GET", "POST"))
@app.route('/browse/', methods=("GET", "POST"))
def browse(query=None,
           language=None):
    '''If guest:  let them browse videos.

    elif user: All of the above plus >
        - Let them browse popular playlists.
        - Create playlists

    todo:
        Common header
        | LanGO | Browse videos | Browse playlists | User profile
    '''

    searchVideoForm = SearchVideoForm()

    languagesNames = list(constants.LANGUAGE_ISO_CODE_MAPPING.keys())

    if searchVideoForm.validate_on_submit():
        searchQueryData = searchVideoForm.searchQuery.data
        languageData = searchVideoForm.language.data
        languageCode = constants.LANGUAGE_ISO_CODE_MAPPING.get(languageData)

        if languageCode:
            return redirect(url_for('browse', query=searchQueryData, language=languageCode))
        else:
            return redirect(url_for('browse', query=searchQueryData))

    if query is None:
        return render_template('browse.html',
                               languages=languagesNames,
                               searchVideoForm=searchVideoForm)

    if language is not None:
        searchResults = youtube.search(query, inLanguageCode=language)
    else:
        searchResults = youtube.search(query)

    return render_template('browse.html',
                           searchVideoForm=searchVideoForm,
                           searchResults=searchResults,
                           languageCode=language,
                           languages=languagesNames)

@app.route('/exercise/<videoId>/<languageCode>', methods=("GET", "POST"))
@app.route('/exercise/<videoId>', methods=("GET", "POST"))
def exercise(videoId=None,
             languageCode=None):

    #todo! enable

    #todo! handle when not providing languageCode here and on videoInfo
    # todo! Cache it! alternatives: session/flask cache rnd
    videoInfo = youtube.getVideoInfo(videoId,
                                     languageCode,
                                     inCheckValidIdBool=True)

    if not videoInfo:
        return 'Not valid url'


    blankExerciseForm = BlankExerciseForm()

    if blankExerciseForm.validate_on_submit():
        progressInt = blankExerciseForm.progress.data or 0
        progressInt += 1

        with urllib.request.urlopen(videoInfo['subtitles']) as response:
            subsXml = xml.etree.ElementTree.parse(response)
            root = subsXml.getroot()
            child = root[progressInt]
            text = child.text
            subStart = float(child.attrib['start'])
            subEnd = subStart + float(child.attrib['dur'])

        return render_template('exercise.html',
                               videoId=videoId,
                               languageCode=languageCode,
                               blankExerciseForm=blankExerciseForm,
                               inProgressInt=progressInt,
                               currentSubtitle=text,
                               start=subStart,
                               end=subEnd)

    return render_template('exercise.html',
                           videoId=videoId,
                           languageCode=languageCode,
                           blankExerciseForm=blankExerciseForm,
                           inProgressInt=0)


if __name__ == "__main__":
    app.run()