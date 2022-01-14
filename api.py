import logging

from sqlalchemy.sql.expression import func

from flask import url_for

import json

import constant.constants
import youtube
import language
import models

from app import db

def getVideoPreviewInfoFromId( inVideoId               ,
                               inForceDBUse     = True ,
                               **inKwargs              ):
    '''
    '''
    videoDB = models.Video.query.get(inVideoId)

    if not videoDB:

        if inForceDBUse:
            return

        videoInfo = youtube.getVideoInfo(inVideoId)

        if not videoInfo:
            return

        videoInfo[youtube.VIDEO_URL_KEY_NAME] = url_for('exercise', videoId=inVideoId)

        for langCode in videoInfo[youtube.SUBTITLES_KEY_NAME].keys():
            videoInfo[youtube.SUBTITLES_KEY_NAME][langCode][
                youtube.EXERCISE_URL_KEY_NAME] = url_for('exercise', videoId=inVideoId, languageCode=langCode)

        return videoInfo

    return getVideoPreviewInfoFromDB(videoDB, **inKwargs)


def getVideoPreviewInfoFromDB( inVideo                 ,
                               inLanguageCodes  = None ,
                               inLimitLanguages = None ,
                               userDB           = None ):
    '''
    '''
    videoId = inVideo.id

    videoDict = {youtube.ID_KEY_NAME: videoId,
                 youtube.TITLE_KEY_NAME: inVideo.title,
                 youtube.SUBTITLES_KEY_NAME: {},
                 youtube.VIDEO_URL_KEY_NAME: url_for('exercise', videoId=videoId),
                 }

    if inLanguageCodes:
        query = inVideo.subtitles.filter(models.Subtitle.language_id.in_(inLanguageCodes ))
    else:
        query = inVideo.subtitles

    if inLimitLanguages:
        query = query.limit( inLimitLanguages )

    for subtitle in query.all():
        langCode = subtitle.languageCode

        videoDict[youtube.SUBTITLES_KEY_NAME][langCode] = {
            'voteCount':
                getVoteCount(subtitle),
            'hasKnownWordsIndexList':
                bool(subtitle.knownWordsIndexList),
            'voted':
                True,
            youtube.EXERCISE_URL_KEY_NAME:
                url_for('exercise', videoId=videoId, languageCode=langCode),
            youtube.EXERCISE_FILL_ALL_URL_KEY_NAME:
                url_for('exercise', videoId=videoId, languageCode=langCode, exerciseType=youtube.EXERCISE_FILL_ALL_URL_KEY_NAME),
            'id':
                subtitle.id,
            youtube.LONG_LANGUAGE_KEY_NAME:
                language.getLongLanguageName(langCode),
        }

        if not userDB:
            continue

        vote = models.Vote.query.filter_by(user=userDB, subtitle=subtitle).first()

        if not vote:
            continue

        videoDict[youtube.SUBTITLES_KEY_NAME][langCode]['userVote'] = vote.upvote

    return videoDict

def getVideoPreviewsInfo(inByLanguages    = None ,
                         inLimitLanguages = None ,
                         inLimitVideos    = constant.constants.RECCOMMENDATIONS_LIMIT ,
                         inUserDB         = None ):
    '''
    Args:
        inByLanguages (list[models.Language]): List of languages' subtitles to retrieve from a video if any.
        inLimitLanguages (int): Limit languages.
    '''
    videos = []

    if inByLanguages:
        languageShortCodes = [x.shortCode for x in inByLanguages]

        for subtitleDB in models.Subtitle.query.filter(
            models.Subtitle.language_id.in_( languageShortCodes ) ).limit( inLimitVideos ).all():

            videoDB = subtitleDB.videoIdLink

            if videoDB in videos:
                continue

            videos.append( getVideoPreviewInfoFromDB( videoDB                               ,
                                                      inLanguageCodes  = languageShortCodes ,
                                                      inLimitLanguages = inLimitLanguages   ,
                                                      userDB           = inUserDB           ) )

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
        for video in models.Video.query.order_by(func.random()).limit(inLimitVideos).all():
            videos.append(
                getVideoPreviewInfoFromDB( video                             ,
                                           inLanguageCodes=inByLanguages     ,
                                           inLimitLanguages=inLimitLanguages ) )

    return videos


def getVideoInfo(inYoutubeId,
                 inLanguageCodes=None,
                 inForceLongCode=True,
                 inForceDBUse=True):
    '''Returns the video's information with the subtitle tracks.

    Checks if passed youtube Id is valid.

    Used for exercise routes.

    Args:
        inYoutubeId (str): video Id.
        inLanguageCodes (list(str)): Language codes list to retrieve subtitle tracks.
        inForceLongName (bool): Force Long code of subtitles. Ex: en-GB.
        inForceDBUse (bool): todo!

    Ex: getVideoInfo('Xou0au6OSZU', ['en-GB'])

    Returns:
        {'title': 'Videogame Discourse is Broken | Design Dive',
         'author_name': 'AI and Games',
         'author_url': 'https://www.youtube.com/c/AIGamesSeries',
         'thumbnail_url': 'https://i.ytimg.com/vi/Xou0au6OSZU/hqdefault.jpg',
         'subtitlesDict':
            {'en-GB': {'transcriptText': [{'text': [['Video games discourse', False], ['is', True], ['broken.', False]], 'start': 0.08, 'duration': 2.24, 'end': 2.32},
             ...
    '''
    # Check for basic info to make sure it can be embedded.
    videoInfoDict = youtube.getVideoBasicInfo(inYoutubeId)

    if not videoInfoDict:
        return

    # Look up video in DB, if not found, fetch from LanGo youtube api.
    videoDB = models.Video.query.get(inYoutubeId)

    if videoDB:

        if not inForceLongCode:
            inLanguageCodes = [lang.split('-')[0] for lang in inLanguageCodes]

        for subtitleDB in videoDB.subtitles.all():

            if inLanguageCodes:
                if inForceLongCode:
                    languageCode = subtitleDB.languageCode
                else:
                    languageCode = subtitleDB.languageCode.split('-')[0]

                if languageCode not in inLanguageCodes:
                    continue

            subDict = {youtube.TRANSCRIPT_TEXT_KEY_NAME       : json.loads(subtitleDB.text)}

            videoInfoDict.setdefault( youtube.SUBTITLES_KEY_NAME ,
                                     {}                          ).setdefault(
                                     subtitleDB.languageCode     ,
                                     subDict                     )

        return videoInfoDict

    else:

        if inForceDBUse:
            return

        return youtube.getVideoInfo(inYoutubeId,
                                    inLanguageCodes=inLanguageCodes)


def getVoteCount(inSubtitleDB):
    voteValues = [vote.upvote for vote in inSubtitleDB.all_sub_votes]
    return voteValues.count(True) - voteValues.count(False)

def storeVideoInfo(inYoutubeId):
    '''Store a video and all its subtitle tracks into the DB.

    If the youtubeId already exists in the DB as the id on the Video table. it will skip.
    '''

    videoDB = models.Video.query.get(inYoutubeId)

    if videoDB:
        logging.error('Skipped youtube id {0}. Already exists on the DB.'.format(inYoutubeId))
        return

    videoInfo = youtube.getVideoInfo(inYoutubeId)

    if not videoInfo:
        return

    videoDB = models.Video(id=inYoutubeId,
                           title=videoInfo['title'])

    db.session.add(videoDB)

    for languageCode, subDict in videoInfo[youtube.SUBTITLES_KEY_NAME].items():

        languageDB = models.Language.query.get(languageCode.split('-')[0])

        if not languageDB:
            logging.info('Skipping language: {0} in video: {1}. Not supported'.format(
                languageCode.split('-')[0],
                inYoutubeId))
            continue

        subList = subDict[youtube.TRANSCRIPT_TEXT_KEY_NAME]

        subTrackDB = models.Subtitle(
            languageCode=languageCode,
            text=json.dumps(subList),
            videoIdLink=videoDB,
            languageLink=languageDB)

        db.session.add(subTrackDB)

    db.session.commit()
