from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

import constants
from forms.videoUrl import VideoUrlForm
from forms.videoSubtitles import VideoSubtitlesForm
from forms.searchVideo import SearchVideoForm

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

@app.route('/browse/<query>/<language>')
@app.route('/browse/<query>/')
@app.route('/browse/')
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

    if query is None:
        return render_template('browse.html',
                               searchVideoForm=searchVideoForm)

    if language is not None:
        searchResults = youtube.search(query, inLanguageCode=language)
    else:
        searchResults = youtube.search(query)

    return render_template('browse.html',
                           searchVideoForm=searchVideoForm,
                           searchResults=searchResults)

@app.route('/exercise/<videoId>/<language>')
def exercise(videoId=None,
             inLanguageCode=None):

    if youtube.isIdValid(videoId, inLanguageCode):
        return render_template('exercise.html')

@app.route("/test", methods=("GET", "POST"))
def addVideo():
    '''Deprecated
    '''
    videoUrlForm = VideoUrlForm()
    videoSubtitlesForm = VideoSubtitlesForm()

    # Video url Post request
    if videoUrlForm.validate_on_submit():
        session['currentTitle'] = videoUrlForm.videoTitle
        session['subtitles'] = videoUrlForm.subtitles
        return redirect(url_for("index"))

    if videoSubtitlesForm.validate_on_submit():
        return redirect(url_for("index"))

    currentTitle = session.get('currentTitle', '')
    isCurrentTitle = bool(currentTitle)

    if isCurrentTitle:
        videoSubtitlesForm.subtitles.choices = session.get('subtitles', [])

    return render_template("index2.html",
                           inCurrentTitle=currentTitle,
                           inVideoUrlForm=videoUrlForm,
                           inVideoSubsForm=videoSubtitlesForm,
                           isConfirm=isCurrentTitle)


if __name__ == "__main__":
    app.run()