from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for, flash, request
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required


import constants
from forms.searchVideo import SearchVideoForm
from forms.videoUrl import VideoUrlForm
from forms.submitExercise import SubmitExerciseForm
from forms.login import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.urls import url_parse

from config import Config
import youtube

DEBUG = True
SECRET_KEY = "secret"

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

import models
import api

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.checkPassword(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return 'REGISTER'

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')


@app.route("/")
@app.route("/index")
def index():
    '''Index page, Let's you sign up/ log in or continue as guest.
    Gets redirected if a session exists.
    '''

    videos = []
    for video in models.Video.query.all():

        videoId = video.id

        videoDict = {youtube.ID_KEY_NAME        : videoId     ,
                     youtube.TITLE_KEY_NAME     : video.title ,
                     youtube.SUBTITLES_KEY_NAME : {}          }

        for subtitle in video.subtitles.all():

            langCode = subtitle.languageCode

            videoDict[youtube.SUBTITLES_KEY_NAME][langCode] = {
                youtube.IS_DEFAULT_TRANSCRIPT_KEY_NAME:
                    subtitle.isDefault,
                youtube.EXERCISE_URL_KEY_NAME:
                    url_for('exercise', videoId=videoId, languageCode=langCode)}

        videos.append(videoDict)

    return render_template("index.html", videos=videos)

@app.route('/browse/<query>/<languageCode>', methods=("GET", "POST"))
@app.route('/browse/<query>/', methods=("GET", "POST"))
@app.route('/browse/', methods=("GET", "POST"))
def browse(query=None,
           languageCode=None):
    '''If guest:  let them browse videos.

    elif user: All of the above plus >
        - Let them browse popular playlists.
        - Create playlists

    TODO!!!!
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
        __populateVideoInfoUrls(videoInfo)

        if not videoInfo:
            return 'Not valid url'

        return render_template('browseUrl.html',
                               videoUrlForm=videoUrlForm,
                               videoInfo=videoInfo)

    return render_template('browseUrl.html', videoUrlForm=videoUrlForm)


@app.route('/exercise/<videoId>/<languageCode>')
@app.route('/exercise', methods=("POST",))
def exercise(videoId=None,
             languageCode=None):
    '''
    '''
    submitExerciseForm = SubmitExerciseForm()

    if submitExerciseForm.validate_on_submit():
        return

    # Look up video in DB, if not, fetch from LanGo youtube api.
    videoInfo = api.getVideoInfo(videoId)

    # todo: Is it needed?
    #__populateVideoInfoUrls(videoInfo)

    if not videoInfo:
        return 'Not valid url'

    if languageCode is None:
        return 'No provided language'

    subDict = videoInfo[youtube.SUBTITLES_KEY_NAME].get(languageCode)

    #todo in API!
    #if not subDict:
    #    return '{0} Not found.'.format(languageCode)

    # todo in API!
    #if videoDB:
    #    subList = subDict[youtube.TRANSCRIPT_OBJ_KEY_NAME]
    #else:
    #    subList = subDict[youtube.TRANSCRIPT_OBJ_KEY_NAME].fetch()

    #TODO! WHY BOTHER!! DO THIS FROM THE BEGINNING
    youtube.formatTranscript(subDict[youtube.TRANSCRIPT_TEXT_KEY_NAME])

    subList = subDict[youtube.TRANSCRIPT_TEXT_KEY_NAME]

    return render_template('exercise.html',
                           videoId=videoId,
                           languageCode=languageCode,
                           subList=subList,
                           submitExerciseForm=submitExerciseForm)

def __populateVideoInfoUrls(inVideoInfo):
    '''
    '''
    for langCode, subDict in inVideoInfo[youtube.SUBTITLES_KEY_NAME].items():
        videoUrl = url_for('exercise',
                           videoId=inVideoInfo['id'],
                           languageCode=langCode)
        subDict[youtube.EXERCISE_URL_KEY_NAME] = videoUrl


@app.shell_context_processor
def make_shell_context():

    def initDatabase():

        import models
        db.drop_all()
        db.create_all()

        print('INITIALIZING DATABASE!')

        heyUser = models.User(username='hey')
        heyUser.setPassword('111')
        db.session.add(heyUser)

        ########## Init database #########################################################
        youtubeLinks = [
            'https://www.youtube.com/watch?v=Xou0au6OSZU',
            'https://www.youtube.com/watch?v=d-xDKpEzmG8',
            'https://www.youtube.com/watch?v=UOgvbS4GkF0',
            'https://www.youtube.com/watch?v=AYEWsLdLmcc&t=272s',
            'https://www.youtube.com/watch?v=YfrVfj2FlW8',
            'https://www.youtube.com/watch?v=QbyGgn4lDi4'
        ]

        for youtubeLink in youtubeLinks:

            youtubeId = youtube.getVideoId(youtubeLink)

            api.storeVideoInfo(youtubeId)

    return { 'db': db            ,
             'i': initDatabase() ,
             #'e': exit()
                                 }

if __name__ == "__main__":
    app.run()