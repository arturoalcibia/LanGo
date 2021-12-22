from  sqlalchemy.sql.expression import func

from flask import url_for, flash, request, jsonify

import json

import constant.constants
import youtube
import language
import models

from app import db

def getVideoPreviewInfo(inVideo):
    videoId = inVideo.id

    videoDict = {youtube.ID_KEY_NAME: videoId,
                 youtube.TITLE_KEY_NAME: inVideo.title,
                 youtube.SUBTITLES_KEY_NAME: {},
                 youtube.VIDEO_URL_KEY_NAME: url_for('exercise', videoId=videoId),
                 }

    for subtitle in inVideo.subtitles.all():
        langCode = subtitle.languageCode

        videoDict[youtube.SUBTITLES_KEY_NAME][langCode] = {
            'voted':
                True,
            youtube.EXERCISE_URL_KEY_NAME:
                url_for('exercise', videoId=videoId, languageCode=langCode),
            'id':
                subtitle.id,
            youtube.LONG_LANGUAGE_KEY_NAME:
                language.getLongLanguageName(langCode),
        }

    return videoDict

def getVideoPreviewsInfo(inByLanguages=None):
    '''
    '''
    videos = []

    if inByLanguages:
        # todo: can it be optimized?
        for languageCode in inByLanguages:
            for video in models.Video.query.filter(
                    models.Video.subtitles.any(
                        languageCode=languageCode)).limit(constant.constants.RECCOMMENDATIONS_LIMIT):
                videos.append(getVideoPreviewInfo(video))

    else:
        '''
        https://stackoverflow.com/questions/11005391/shuffling-sqlalchemy-results/11007820
        
        if you are using MySQL, you can do:
            from sqlalchemy.sql.expression import func
            Item.query.order_by(func.rand()).offset(20).limit(10).all()
        
        Or, in PostgreSQL:
            from sqlalchemy.sql.expression import func
            Item.query.order_by(func.random()).offset(20).limit(10).all()
        '''
        for video in models.Video.query.order_by(func.random()).limit(2).all():
            videos.append(getVideoPreviewInfo(video))

    return videos

def getVideoInfo(inYoutubeId,
                 inLanguageCode=None):
    '''Checks if passed youtube Id is valid. Returns a video's information.

    Args:
        inYoutubeId (str): video Id.

        inLanguageCode (str): Language code to check if available as a subtitle. If not, return None.
        inOnlyManualSubtitlesBool (str): Retrieve only manually created subtitles.
        inVideoDB (models.Video): Video database object to locally query all video Info.
    '''
    # Check for basic info to make sure it can be embedded.
    videoInfoDict = youtube.getVideoBasicInfo(inYoutubeId)

    if not videoInfoDict:
        return

    # Look up video in DB, if not found, fetch from LanGo youtube api.
    videoDB = models.Video.query.get(inYoutubeId)

    if videoDB:
        for subtitleDB in videoDB.subtitles.all():

            if inLanguageCode and inLanguageCode != subtitleDB.languageCode:
                continue

            subDict = {youtube.TRANSCRIPT_TEXT_KEY_NAME       : json.loads(subtitleDB.text)}

            videoInfoDict.setdefault( youtube.SUBTITLES_KEY_NAME ,
                                     {}                          ).setdefault(
                                     subtitleDB.languageCode     ,
                                     subDict                     )
    else:
        #todo!
        pass

    return videoInfoDict

def storeVideoInfo(inYoutubeId):
    '''
    '''

    videoDB = models.Video.query.get(inYoutubeId)

    if videoDB:
        return

    videoInfo = youtube.getVideoInfo(inYoutubeId)

    if not videoInfo:
        return

    videoDB = models.Video(id=inYoutubeId,
                           title=videoInfo['title'])

    db.session.add(videoDB)

    for languageCode, subDict in videoInfo[youtube.SUBTITLES_KEY_NAME].items():

        subList = subDict[youtube.TRANSCRIPT_OBJ_KEY_NAME].fetch()
        #todo!! Improve structure!
        youtube.formatTranscript(subList)

        subTrackDB = models.Subtitle(
            languageCode=languageCode,
            languageShortCode=languageCode.split('-')[0],
            text=json.dumps(subList),
            videoIdLink=videoDB)

        db.session.add(subTrackDB)

    db.session.commit()
