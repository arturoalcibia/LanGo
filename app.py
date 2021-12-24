####### todo!!!: add languages to profile sign up/ profile page!

from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for, flash, request, jsonify
from flask_login import LoginManager
from flask_login import login_user, current_user, login_required

from constant import constants
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

    if current_user.is_authenticated:
        videos = api.getVideoPreviewsInfo()
    else:
        #videos = api.getVideoPreviewsInfo(inByLanguages=['es', 'en'])
        videos = api.getVideoPreviewsInfo( inLimitLanguages = 2 )

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

@app.route('/exercise', methods=("POST",))
@app.route('/exercise/<videoId>')
@app.route('/exercise/<videoId>/<languageCode>')
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

    return render_template('exercise.html',
                           videoId=videoId,
                           languageCode=languageCode,
                           subList=subDict[youtube.TRANSCRIPT_TEXT_KEY_NAME],
                           submitExerciseForm=submitExerciseForm)

def __populateVideoInfoUrls(inVideoInfo):
    '''
    '''
    for langCode, subDict in inVideoInfo[youtube.SUBTITLES_KEY_NAME].items():
        videoUrl = url_for('exercise',
                           videoId=inVideoInfo['id'],
                           languageCode=langCode)
        subDict[youtube.EXERCISE_URL_KEY_NAME] = videoUrl

@app.route("/vote/<int:inSubtitleId>/<inVoteValue>")
def vote(inSubtitleId,
         inVoteValue):

    if not current_user.is_authenticated:
        return '', 403

    inSubIdDB = models.Subtitle.query.get_or_404(inSubtitleId)
    vote = models.Vote.query.filter_by(user=current_user, subtitle=inSubIdDB).first()
    valueBool = True if inVoteValue == 'upvote' else False

    if vote:
        if vote.upvote != valueBool:
            vote.upvote = valueBool
            db.session.commit()
        else:
            return '', 403

    else:
        vote = models.Vote(user=current_user, subtitle=inSubIdDB, upvote=bool(inVoteValue))
        db.session.add(vote)
        db.session.commit()

    return '', 200

@app.route('/votecount/<int:inSubtitleId>')
def getVotes(inSubtitleId):

    if not current_user.is_authenticated:
        return '', 403

    inSubIdDB = models.Subtitle.query.get_or_404(inSubtitleId)

    voteValues = [vote.upvote for vote in inSubIdDB.all_sub_votes]
    return jsonify(voteValues.count(True) - voteValues.count(False)), 200


@app.route('/contact')
def contact():

    # todo! if logged in no need to display email and name, display them as hidden instead.
    return render_template(
        'contact.html',
        inGoogleForm='https://docs.google.com/forms/d/e/1FAIpQLSfKX9L1mJ1A-xLANA3LH9RKJvs-gYELVDLFu9XN3leUKhjUDw',
        inNameId=1857853291,
        inEmailId=1674025034,
        inCommentId=1749810715)

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