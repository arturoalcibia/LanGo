import json

import youtube
import models

from app import db

def getVideoInfo(inYoutubeId,
                 inLanguageCode=None,
                 inOnlyManualSubtitlesBool=True):
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

            subDict = {youtube.TRANSCRIPT_TEXT_KEY_NAME       : json.loads(subtitleDB.text) ,
                       youtube.IS_DEFAULT_TRANSCRIPT_KEY_NAME : True                        } # todo!

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

    #todo! Why can't we use obj above?
    videoDB = models.Video.query.get(inYoutubeId)

    for languageCode, subDict in videoInfo[youtube.SUBTITLES_KEY_NAME].items():
        subTrackDB = models.Subtitle(
            languageCode=languageCode,
            isDefault=bool(subDict[youtube.IS_DEFAULT_TRANSCRIPT_KEY_NAME]),
            text=models.Subtitle.dictToString(subDict[youtube.TRANSCRIPT_OBJ_KEY_NAME].fetch()),
            videoIdLink=videoDB)

        db.session.add(subTrackDB)

    db.session.commit()
