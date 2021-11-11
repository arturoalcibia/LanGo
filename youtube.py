import re
import requests

from youtubesearchpython import *
from youtube_transcript_api import YouTubeTranscriptApi

import constants
import language

# Used to validate a youtube url and extract it's videoId.
YOUTUBE_URL_RE = re.compile('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)(?P<code>[\w\-]+)(\S+)?$')

# Video title key name, extracted from getVideoBasicInfo Fn.
TITLE_KEY_NAME = 'title'

# Video thumbnail key name, extracted from getVideoBasicInfo Fn.
THUMBNAIL_URL_KEY_NAME = 'thumbnail_url'

#todo!
DEFAULT_LANG_NAME = 'defaultLang'

# Video subtitles info key name, extracted from  YouTubeTranscriptApi.list_transcripts Fn.
SUBTITLES_KEY_NAME = 'subtitlesDict'

#todo!
DEFAULT_LANGUAGE_KEY_NAME = 'defaultLanguage'

#todo!
EXERCISE_URL_KEY_NAME = 'exerciseUrl'

# Transcript obj name, extracted from  YouTubeTranscriptApi.list_transcripts. Fn.
TRANSCRIPT_OBJ_KEY_NAME = 'transcriptObj'


def formatTranscript(inTranscriptList):
    ''' Format transcript by:
            - Adding end float key per text.
            - Replacing the text str to a list with each word.

    * Currently coming from YouTubeTranscriptApi.Transcript.fetch Fn.

    Args:
        inTranscriptList (list):
            Ex:
                [{'text': str, 'start': float, 'duration': float}].

    New format:
        List: [{'text': list[str],
                'start': float,
                'end': float,
                'duration': float}].
    '''
    for subDict in inTranscriptList:

        subDict['text'] = language.splitSentence(subDict['text'])
        startFloat = float(subDict['start'])
        subDict['end'] = round(float(subDict['duration']) + startFloat, 2)


def getVideoBasicInfo(inVideoId):
    '''Does a quick request to check for its availability to embed, if it's not private.

    Args:
        inVideoId (str): video Id.

    Returns:
        dict: Youtube response.
            Ex:
                {"title":"La Hora Feliz",
                "author_name":"Cojo Feliz",
                "author_url":"https://www.youtube.com/user/cojofeliz",
                "thumbnail_url":"https://i.ytimg.com/vi/yJhBISGvt08/hqdefault.jpg",
                ...} #todo! prune!
    '''
    requestUrl = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={0}'.format(
        inVideoId)
    requestObj = requests.get(url=requestUrl)

    # Match if video is not available/private/exists.
    if not requestObj.status_code != '200':
        return None

    if requestObj.text == 'Unauthorized':
        return None

    return requestObj.json()

def getVideoInfo(inYoutubeId,
                 inLanguageCode=None,
                 inOnlyManualSubtitlesBool=True):
    '''Checks if passed youtube Id is valid. Returns a video's information.

    Args:
        inYoutubeId (str): video Id.
        inLanguageCode (str): Language code to check if available as a subtitle. If not, return None.
        inOnlyManualSubtitlesBool (str): Retrieve only manually created subtitles. todo!

    Returns:

        {'title': 'Test!',
        'author_name': "Rachel's English",
        'author_url': 'https://www.youtube.com/c/rachelsenglish',
        'thumbnail_url': 'https://i.ytimg.com/vi/t6bbuDUPIgk/hqdefault.jpg',
        'id': 't6bbuDUPIgk',
        'link': 'https://www.youtube.com/watch?v=t6bbuDUPIgk',
        'subtitlesDict':
            {'af':
                {'transcriptObj': <youtube_transcript_api._transcripts.Transcript object at 0x00...>},
            ...
        }

    '''
    videoInfoDict = getVideoBasicInfo(inYoutubeId)

    if not videoInfoDict:
        return

    videoInfoDict['id'] = inYoutubeId
    youtubeLink = 'https://www.youtube.com/watch?v={0}'.format(inYoutubeId)
    videoInfoDict['link'] = youtubeLink

    transcripts = YouTubeTranscriptApi.list_transcripts(inYoutubeId)

    manuallyCreatedTranscriptsDict = transcripts._manually_created_transcripts

    if inOnlyManualSubtitlesBool:

        if not manuallyCreatedTranscriptsDict:
            return

        if inLanguageCode and inLanguageCode not in manuallyCreatedTranscriptsDict.keys():
            return

    videoInfoDict[SUBTITLES_KEY_NAME] = {key:{TRANSCRIPT_OBJ_KEY_NAME:transcriptObj}
                                         for key, transcriptObj
                                         in manuallyCreatedTranscriptsDict.items()}

    return videoInfoDict

def getVideoId(inUrl):
    '''Extract youtube id from a youtube url.

    Args:
        inUrl (str): youtube url.
            Can be formatted in multiple ways and arguments.

    Returns:
        None | str: videoId.
    '''
    urlMatch = YOUTUBE_URL_RE.match(inUrl)

    if not urlMatch:
        return

    return urlMatch.group('code')  # Ex: cAoR6FUE0kk

def search(inSearchStr,
           inLanguageCode=None,
           inLimit=constants.SEARCH_LIMIT):

    searchResults = []
    retryCounter = 0

    #todo! limit dooooo constant
    ytSearch = CustomSearch(inSearchStr, 'EgQQASgB', limit=20)

    #todo! DOESNT STOP WHEN REACHED TO LIMIT
    while len(searchResults) < inLimit or retryCounter < constants.RETRY_LIMIT:
        for videoInfoDict in ytSearch.result()['result']:

            getVideoInfoKwargs = {}

            if False:
                getVideoInfoKwargs['inLanguageCode'] = inLanguageCode

            videoInfo = getVideoInfo(videoInfoDict['id'])

            if videoInfo:
                searchResults.append(videoInfo)

        retryCounter += 1
        ytSearch.next()

    return searchResults
