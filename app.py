from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request

import constants
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

@app.route('/exercise/<videoId>/<languageCode>')
@app.route('/exercise/<videoId>/')
def exercise(videoId=None,
             languageCode=None):
    if youtube.isIdValid(videoId, languageCode):
        return render_template('exercise.html', videoId=videoId, languageCode=languageCode)

    #todo! render template for invalid videoId
    return 'Not valid url'


if __name__ == "__main__":
    app.run()