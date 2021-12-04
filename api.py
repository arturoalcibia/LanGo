import json

import youtube
import models

def getVideoInfo(inYoutubeId,
                 **inKwargs):
    '''Checks if passed youtube Id is valid. Returns a video's information.

    Args:
        inYoutubeId (str): video Id.

        inLanguageCode (str): Language code to check if available as a subtitle. If not, return None.
        inOnlyManualSubtitlesBool (str): Retrieve only manually created subtitles.
        inVideoDB (models.Video): Video database object to locally query all video Info.
    '''

    inLanguageCode = inKwargs.get('inLanguageCode')
    inOnlyManualSubtitlesBool = inKwargs.get('inOnlyManualSubtitlesBool')
    inVideoDB = inKwargs.get('inVideoDB')

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
        youtube.getVideoInfo()

    return videoInfoDict