import requests

import youtube_dl
from youtubesearchpython import *

import constants

def getVideoInfo(inYoutubeId,
                 inLanguageCode=None,
                 inCheckValidIdBool=False):

    if inCheckValidIdBool and not isIdValid(inYoutubeId):
        return

    # todo: naming is not the best!
    # todo! this is being repeated

    # Some videos that are about to go live will error.
    try:
        with youtube_dl.YoutubeDL({}) as ydl:

            #todo! move to specific fn.
            youtubeLink = 'https://www.youtube.com/watch?v={0}'.format(inYoutubeId)

            videoInfo = ydl.extract_info(youtubeLink, download=False)

            videoInfoDict = {'link': youtubeLink,
                             'title': videoInfo['title'],
                             'id': videoInfo['id']}

            if inLanguageCode:

                closestLanguage = getClosestLanguage(
                    videoInfo['subtitles'].keys(),
                    inLanguageCode)

                if not closestLanguage:
                    return

                videoInfoDict['subtitles'] = videoInfo['subtitles'][closestLanguage][0]['url']

            return videoInfoDict

    except:
        # todo! narrow down?
        return

def getClosestLanguage(inVideoLanguages,
                       inRequestedCodeLanguage):
    '''Get closest language
    todo!
    '''
    for videoLangCode in inVideoLanguages:

        # Ex: convert 'Es-Mx' to 'es', return first match.
        if inRequestedCodeLanguage == videoLangCode.lower().split('-')[0]:
            return videoLangCode


def isIdValid(inYoutubeId,
              inLanguageCode=None):
    requestUrl = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={0}'.format(
        inYoutubeId)
    requestObj = requests.get(url=requestUrl)

    # Match if video is not available/private/exists.
    if not requestObj.status_code != '200':
        return False

    if requestObj.text == 'Unauthorized':
        return False

    print(requestObj.text)

    link = 'https://www.youtube.com/watch?v={0}'.format(inYoutubeId)

    videoInfoKwargs = {}

    if inLanguageCode:
        inLanguage = constants.ISO_CODE_LANGUAGE_MAPPING[inLanguageCode]
        videoInfoKwargs['inLanguageCode'] = inLanguage

    return bool(getVideoInfo(inYoutubeId, **videoInfoKwargs))

def search(inSearchStr,
           inLanguageCode=None,
           inLimit=constants.SEARCH_LIMIT):

    searchResults = []
    retryCounter = 0

    ytSearch = CustomSearch(inSearchStr, 'EgQQASgB', limit=inLimit)

    while not searchResults and retryCounter < constants.SEARCH_LIMIT:
        for videoInfoDict in ytSearch.result()['result']:

            videoInfo = getVideoInfo(videoInfoDict['id'], inLanguageCode=inLanguageCode)

            if videoInfo:
                searchResults.append(videoInfo)

        retryCounter += 1
        ytSearch.next()

    return searchResults

