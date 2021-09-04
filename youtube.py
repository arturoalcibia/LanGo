import threading

import youtube_dl
from youtubesearchpython import *

import constants

def getVideoInfo(inYoutubeLink,
                 inLanguage,
                 inFallbackToRoot=True):
    # todo: naming is not the best!
    # Some videos that are about to go live will error.

    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            videoInfo = ydl.extract_info(inYoutubeLink, download=False)

            if not isLanguageRequested(videoInfo['subtitles'].keys(),
                                       inLanguage,
                                       inFallbackToRoot=inFallbackToRoot):
                return

            print('######################################')
            print(inLanguage)
            print(videoInfo['subtitles'].keys())
            print('######################################')

            return {'link': inYoutubeLink,
                    'title': videoInfo['title']}

    except:
        # todo! narrow down?
        return None

def isLanguageRequested(inVideoLanguages,
                        inRequestedLanguageStr,
                        inFallbackToRoot=True):
    '''Checks if video corresponds to requested subtitle language.

    Args:

        inFallbackToRoot: If "Spanish (Mexico)" is requested, will also consider
        "Spanish" as valid.
    '''
    inVideoLanguages = [lang.lower() for lang in inVideoLanguages]

    languageCode = constants.ISO_LANGUAGE_CODE_MAPPING[inRequestedLanguageStr]

    if languageCode in inVideoLanguages:
        return True

    if inFallbackToRoot:
        languageCode = languageCode.split('-')

        if len(languageCode) != 2:
            return False

        genericLangs = set()

        for lang in inVideoLanguages:

            splitLang = lang.split('-')

            if len(splitLang) == 2:
                genericLangs.add(splitLang[0])
                continue

            genericLangs.add(lang)

        # Ex: 'fr-ca' to 'fr'
        if languageCode[0] in inVideoLanguages:
            return True

    return False

def search(inSearchStr,
           inLanguage,
           inLimit=constants.SEARCH_LIMIT):

    searchResults = []
    retryCounter = 0


    ytSearch = CustomSearch(inSearchStr, 'EgQQASgB', limit=inLimit)

    threads = []

    while not searchResults and retryCounter < constants.SEARCH_LIMIT:
        for videoInfoDict in ytSearch.result()['result']:


            link = 'https://www.youtube.com/watch?v={0}'.format(videoInfoDict['id'])
            '''
            # todo: threading@!
            thread = threading.Thread(target=getVideoInfo, args=(link, inLanguage))
            threads.append(thread)
            thread.start()
            '''

            videoInfo = getVideoInfo(link, inLanguage, inFallbackToRoot=True)
            if videoInfo:
                searchResults.append(videoInfo)


        retryCounter += 1
        ytSearch.next()

    return searchResults

