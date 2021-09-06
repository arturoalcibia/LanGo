import requests

import youtube_dl
from youtubesearchpython import *

import constants

def getVideoInfo(inYoutubeLink,
                 inLanguageCode=None):
    # todo: naming is not the best!
    # todo! this is being repeated
    # Some videos that are about to go live will error.
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            videoInfo = ydl.extract_info(inYoutubeLink, download=False)

            if inLanguageCode is not None and not isLanguageRequested(videoInfo['subtitles'].keys(),
                                                                      inLanguageCode):
                return

            return {'link': inYoutubeLink,
                    'title': videoInfo['title'],
                    'id': videoInfo['id']}

    except:
        # todo! narrow down?
        return None

def isLanguageRequested(inVideoLanguages,
                        inRequestedCodeLanguage):
    '''Checks if video corresponds to requested subtitle language.
    '''

    # Ex: convert 'Es-Mx' to 'es'
    inVideoLanguages = [lang.lower().split('-')[0] for lang in inVideoLanguages]

    return inRequestedCodeLanguage in inVideoLanguages

def isIdValid(inYoutubeId,
              inLanguageCode=None):

    requestUrl = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={0}'.format(
        inYoutubeId)
    requestObj = requests.get(url=requestUrl)

    # Match if video is available/ not private/ exists.
    if not requestObj.status_code != '200':
        return False

    if requestObj.text == 'Unauthorized':
        return False

    link = 'https://www.youtube.com/watch?v={0}'.format(inYoutubeId)

    videoInfoKwargs = {}

    if inLanguageCode:
        inLanguage = constants.ISO_CODE_LANGUAGE_MAPPING[inLanguageCode]
        videoInfoKwargs['inLanguageCode'] = inLanguage

    videoInfo = getVideoInfo(link, **videoInfoKwargs)

    if videoInfo:
        return True

def search(inSearchStr,
           inLanguageCode=None,
           inLimit=constants.SEARCH_LIMIT):

    searchResults = []
    retryCounter = 0

    ytSearch = CustomSearch(inSearchStr, 'EgQQASgB', limit=inLimit)

    while not searchResults and retryCounter < constants.SEARCH_LIMIT:
        for videoInfoDict in ytSearch.result()['result']:

            link = 'https://www.youtube.com/watch?v={0}'.format(videoInfoDict['id'])

            videoInfo = getVideoInfo(link, inLanguageCode=inLanguageCode)

            if videoInfo:
                searchResults.append(videoInfo)

        retryCounter += 1
        ytSearch.next()

    return searchResults

getVideoInfo('https://www.youtube.com/watch?v=5MgBikgcWnY')