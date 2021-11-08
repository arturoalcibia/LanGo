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
    #todo!
    # If signed skip to next page

    return render_template("index.html")

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

        videoInfo = youtube.getVideoInfo(videoId,
                                         inCheckValidIdBool=True)

        if not videoInfo:
            return 'Not valid url'

        # Subtitle name: url
        # Type: {str: str}.
        subtitlesDict = {}
        for subtitleName in youtube.getSubtitleLanguages(videoId, inLongName=True):
            languageCode = constants.LANGUAGE_ISO_CODE_MAPPING.get(subtitleName)
            videoUrl = url_for('exercise',
                               videoId=videoId,
                               languageCode=languageCode)
            subtitlesDict[subtitleName] = videoUrl

        videoInfo[youtube.SUBTITLES_KEY_NAME] = subtitlesDict

        return render_template('browseUrl.html',
                               videoInfo=videoInfo,
                               videoUrlForm=videoUrlForm,
                               subtitlesDict=subtitlesDict)

    return render_template('browseUrl.html', videoUrlForm=videoUrlForm)


@app.route('/detailedVideo/')
def detailedVideo():
    '''
    '''
    videoId = 'Q8Sq9r50gc0'
    videoInfo = youtube.getVideoBasicInfo(videoId)
    videoInfo[youtube.VIDEO_ID_KEY_NAME] = videoId

    # Subtitle name: url
    # Type: {str: str}.
    subtitlesDict = {}
    for subtitleName in youtube.getSubtitleLanguages(videoId, inLongName=True):
        languageCode = constants.LANGUAGE_ISO_CODE_MAPPING.get(subtitleName)
        videoUrl = url_for('exercise',
                           videoId=videoId,
                           languageCode=languageCode)
        subtitlesDict[subtitleName] = videoUrl

    return render_template('_detailedVideo.html',
                           videoInfo=videoInfo,
                           subtitlesDict=subtitlesDict)


@app.route('/exercise/<videoId>/<languageCode>', methods=("GET", "POST"))
@app.route('/exercise/<videoId>/', methods=("GET", "POST"))
def exercise(videoId=None,
             languageCode=None):

    #todo! handle when not providing languageCode here and on videoInfo
    # todo! Cache it! alternatives: session/flask cache rnd
    videoInfo = youtube.getVideoInfo(videoId,
                                     languageCode,
                                     inCheckValidIdBool=True)

    if not videoInfo:
        return 'Not valid url'

    #todo! do exercise page to choose language!!!
    if languageCode is None:
        return 'No provided language'

    subList = youtube.getSubtitlesList(videoInfo['subtitles'])

    return render_template('exercise.html',
                           videoId=videoId,
                           languageCode=languageCode,
                           subList=subList)

if __name__ == "__main__":
    app.run()