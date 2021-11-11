# todo! Cache it! alternatives: session/flask cache rnd
# todo! do exercise page to choose language!!!

import urllib.request
import xml.etree.ElementTree

from flask import Flask
from flask import redirect
from flask import jsonify
from flask import render_template
from flask import session
from flask import url_for
from flask import request

import constants
from forms.searchVideo import SearchVideoForm
from forms.videoUrl import VideoUrlForm

import youtube

DEBUG = True
SECRET_KEY = "secret"

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/header")
def header():
    return render_template("header.html")

@app.route("/")
@app.route("/index")
def index():
    '''Index page, Let's you sign up/ log in or continue as guest.
    Gets redirected if a session exists.
    '''
    videos = youtube.search('test')

    subVideos = []

    for videoInfo in videos:

        videoId = videoInfo['id']
        # Subtitle name: url
        # Type: {str: str}.
        subtitlesDict = youtube.getSubtitleLanguages(videoId)

        if not subtitlesDict:
            continue

        for langCode, subDict in youtube.getSubtitleLanguages(videoId).items():

            languageCode = constants.LANGUAGE_ISO_CODE_MAPPING.get(langCode)

            videoUrl = url_for('exercise',
                               videoId=videoId,
                               languageCode=languageCode)

            subtitlesDict[langCode][youtube.EXERCISE_URL_KEY_NAME] = videoUrl

        videoInfo[youtube.SUBTITLES_KEY_NAME] = subtitlesDict

        subVideos.append(videoInfo)

    return render_template("index.html", videos=subVideos)

@app.route('/browse/<query>/<languageCode>', methods=("GET", "POST"))
@app.route('/browse/<query>/', methods=("GET", "POST"))
@app.route('/browse/', methods=("GET", "POST"))
def browse(query=None,
           languageCode=None):
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
            return redirect(url_for('browse', query=searchQueryData, languageCode=languageCode))
        else:
            return redirect(url_for('browse', query=searchQueryData))

    if query is None:
        return render_template('browse.html',
                               languages=languagesNames,
                               searchVideoForm=searchVideoForm)

    if languageCode is not None:
        searchResults = youtube.search(query, inLanguageCode=languageCode)
    else:
        searchResults = youtube.search(query)

    return render_template('browse.html',
                           searchVideoForm=searchVideoForm,
                           searchResults=searchResults,
                           languageCode=languageCode,
                           languages=languagesNames)

@app.route('/browseurl/', methods=("GET", "POST"))
@app.route('/browseurl/<videoId>', methods=("GET", "POST"))
def browseUrl(videoId=None):
    '''
    '''

    videoUrlForm = VideoUrlForm()

    if videoUrlForm.validate_on_submit():
        return redirect(url_for('browseUrl', videoId=videoUrlForm.VIDEO_ID))

    if videoId:
        videoInfo = youtube.getVideoInfo(videoId)

        if not videoInfo:
            return 'Not valid url'

        for langCode, subDict in videoInfo[youtube.SUBTITLES_KEY_NAME].items():

            videoUrl = url_for('exercise',
                               videoId=videoId,
                               languageCode=langCode)

            subDict[youtube.EXERCISE_URL_KEY_NAME] = videoUrl

        return render_template('browseUrl.html',
                               videoUrlForm=videoUrlForm,
                               videoInfo=videoInfo)

    return render_template('browseUrl.html', videoUrlForm=videoUrlForm)


@app.route('/exercise/<videoId>/<languageCode>')
@app.route('/exercise/<videoId>/')
def exercise(videoId=None,
             languageCode=None):
    '''
    '''
    videoInfo = youtube.getVideoInfo(videoId,
                                     inLanguageCode=languageCode)

    if not videoInfo:
        return 'Not valid url'

    if languageCode is None:
        return 'No provided language'

    subList = videoInfo[youtube.SUBTITLES_KEY_NAME][languageCode][youtube.TRANSCRIPT_OBJ_KEY_NAME].fetch()
    youtube.formatTranscript(subList)

    return render_template('exercise.html',
                           videoId=videoId,
                           languageCode=languageCode,
                           subList=subList)

if __name__ == "__main__":
    app.run()