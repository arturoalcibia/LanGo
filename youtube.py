import functools
import re
import requests

from youtubesearchpython import *
import youtube_transcript_api

from constant import constants
import language

YOUTUBE_URL_RE = re.compile('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)(?P<code>[\w\-]+)(\S+)?$')

# Video title key name, extracted from getVideoBasicInfo Fn.
ID_KEY_NAME = 'id'

# Video title key name, extracted from getVideoBasicInfo Fn.
TITLE_KEY_NAME = 'title'

# Video subtitles info key name, extracted from  YouTubeTranscriptApi.list_transcripts Fn.
SUBTITLES_KEY_NAME = 'subtitlesDict'

#todo!
EXERCISE_URL_KEY_NAME = 'exerciseUrl'

EXERCISE_FILL_ALL_URL_KEY_NAME = 'exerciseFillAllUrl'

EXERCISE_TYPES = (EXERCISE_FILL_ALL_URL_KEY_NAME,)

VIDEO_URL_KEY_NAME = 'videoUrl'

LONG_LANGUAGE_KEY_NAME = 'longLanguage'

# Transcript obj name, extracted from  YouTubeTranscriptApi.list_transcripts. Fn.
TRANSCRIPT_OBJ_KEY_NAME = 'transcriptObj'

# Transcript text name. Stored in the DB as text.
TRANSCRIPT_TEXT_KEY_NAME = 'transcriptText'

@functools.lru_cache(maxsize=None)
def getVideoBasicInfo(inVideoId):
    '''Does a quick request to check for its availability to embed, if it's not private.

    Args:
        inVideoId (str): video Id.

    #todo! prune! This returns unneccessary info!!!

    Returns:
        dict: Youtube response.
            Ex:
                {"title":"La Hora Feliz",
                "author_name":"Cojo Feliz",
                "author_url":"https://www.youtube.com/user/cojofeliz",
                "thumbnail_url":"https://i.ytimg.com/vi/yJhBISGvt08/hqdefault.jpg",
                ...}
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

@functools.lru_cache(maxsize=None)
def getVideoInfo(inYoutubeId,
                 inLanguageCodes=None):
    '''Checks if passed youtube Id is valid. Returns a video's information.

    Args:
        inYoutubeId (str): video Id.
        inLanguageCode (str): Language code to check if available as a subtitle. If not, return None.

    Returns:

        {'title': 'Test!',
        'author_name': "Rachel's English",
        'author_url': 'https://www.youtube.com/c/rachelsenglish',
        'thumbnail_url': 'https://i.ytimg.com/vi/t6bbuDUPIgk/hqdefault.jpg',
        'id': 't6bbuDUPIgk',
        'link': 'https://www.youtube.com/watch?v=t6bbuDUPIgk',
        'subtitlesDict':
            {'af':
                {'transcriptObj': <youtube_transcript_api._transcripts.Transcript object at 0x00...>}, #todo: const!
                {'isDefault': bool}
            ...
        }
    '''
    videoInfoDict = getVideoBasicInfo(inYoutubeId)

    if not videoInfoDict:
        return

    videoInfoDict['id'] = inYoutubeId
    youtubeLink = 'https://www.youtube.com/watch?v={0}'.format(inYoutubeId)
    videoInfoDict['link'] = youtubeLink
    try:
        transcripts = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(inYoutubeId)
    except youtube_transcript_api._errors.TranscriptsDisabled:
        return

    videoInfoDict[SUBTITLES_KEY_NAME] = {}

    print(transcripts._manually_created_transcripts.keys())
    print(inLanguageCodes)

    for langCode, transcriptObj in transcripts._manually_created_transcripts.items():

        if inLanguageCodes and langCode not in inLanguageCodes:
            continue

        subList = transcriptObj.fetch()

        for index, subDict in enumerate(subList):
            subDict['text'] = language.stripPunctuation(subDict['text'])
            subDict["end"] = round(subDict["start"] + subDict["duration"], 2)
            subDict["index"] = index


        videoInfoDict[SUBTITLES_KEY_NAME][langCode] = {TRANSCRIPT_TEXT_KEY_NAME: subList}

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
