from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

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

@app.route('/browse', methods=('GET', 'POST'))
def browse():
    '''If guest:  let them browse videos.

    elif user: All of the above plus >
        - Let them browse popular playlists.
        - Create playlists

    todo:
        Common header
        | LanGO | Browse videos | Browse playlists | User profile
    '''
    searchVideoForm = SearchVideoForm()

    if searchVideoForm.validate_on_submit():

        searchQueryData = searchVideoForm.searchQuery.data
        languageData = searchVideoForm.language.data
        videosSearch = youtube.search(searchQueryData, languageData)

        return render_template('browse.html',
                               searchVideoForm=searchVideoForm,
                               searchResults=videosSearch)

    return render_template('browse.html',
                           searchVideoForm=searchVideoForm)

@app.route('/exercise', methods=('GET', 'POST'))
def exercise():
    searchVideoForm = SearchVideoForm()
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