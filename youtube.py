import requests
import urllib.request
import xml.etree.ElementTree

from youtubesearchpython import *

import constants
# todo ! wtf
import constant.spanish

def __splitSentence(inSentence):

    # List with a portion of the sentence as index 0
    # and true if hint, false if blank as index 1.
    # type: list[list[str, bool]]
    wordTuples = []

    # List to be used as an index to slice the sentence.
    # type: list[int]
    wordIndices = []

    splittedSentence = inSentence.split(' ')

    # Define if word will be a hint or blank.
    lastIndex = 0
    for index, word in enumerate(splittedSentence):
        # Skip every other word.
        if (index % 2) == 0:
            continue

        if word in constant.spanish.words:
            wordIndices.append(index)

    lastSlicedWordIndex = None
    for listIndex, wordIndex in enumerate(wordIndices):

        # If first iteration. Add first part of the string. If any. <<<
        if listIndex == 0 and wordIndex > 0:
            wordTuples.append(
                (' '.join(splittedSentence[:wordIndex]),
                 False))

        # Add any previous leftover strings as hints. If any.
        if lastSlicedWordIndex is not None:

            joinedSentence = None
            wordIndexDifference = wordIndex - lastSlicedWordIndex

            if wordIndexDifference > 2:
                joinedSentence = ' '.join(splittedSentence[lastSlicedWordIndex + 1:wordIndex])

            elif wordIndexDifference > 1:
                joinedSentence = splittedSentence[lastSlicedWordIndex + 1]

            if joinedSentence is not None:
                wordTuples.append((joinedSentence, False))

        wordTuples.append((splittedSentence[wordIndex], True))
        lastSlicedWordIndex = wordIndex

        # If last iteration, add last part of string. >>>
        if listIndex + 1 == len(wordIndices):
            wordTuples.append(
                (' '.join(splittedSentence[wordIndex + 1:]),
                 False))

    # If no words were added as blanks, add the whole sentence as hint.
    if not wordTuples:
        wordTuples.append((inSentence, False))

    return wordTuples

def getClosestLanguage(inVideoLanguages,
                       inRequestedCodeLanguage):
    '''Get closest language
    todo!
    '''
    for videoLangCode in inVideoLanguages:

        # Ex: convert 'Es-Mx' to 'es', return first match.
        if inRequestedCodeLanguage == videoLangCode.lower().split('-')[0]:
            return videoLangCode

def getSubtitleLanguages(inVideoId):
    '''
    '''
    subVideoUrl = 'https://video.google.com/timedtext?v={0}&type=list'.format(inVideoId)

    requestObj = requests.get(url=subVideoUrl)
    languages = []

    # Match if video is not available/private/exists.
    if not requestObj.status_code != '200':
        return None

    for child in xml.etree.ElementTree.fromstring(requestObj.content).iter('*'):

        if not child.tag == 'track':
            continue

        languages.append(child.attrib['lang_code'])

    return languages

def getSubtitlesList(inSubtitlesUrl):
    '''

    Returns:
         dict:
            dict{'end'  : float ,
                 'start': float ,
                 'text' : [ [ str , bool ] ] }
    '''
    with urllib.request.urlopen(inSubtitlesUrl) as response:
        subsXml = xml.etree.ElementTree.parse(response)
        subRoot = subsXml.getroot()
        subs = []
        for xmlElement in subRoot:

            start = xmlElement.attrib['start']

            # Used to precise display
            startFloat = float(start)

            wordTuples = __splitSentence(xmlElement.text)

            subs.append({'end': round(float(xmlElement.attrib['dur']) + startFloat, 2),
                         'start': startFloat,
                         'text': wordTuples})

        return subs

def getVideoBasicInfo(inYoutubeId):
    '''
    todo!
    Also checks if video is available to embed.
    '''
    requestUrl = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={0}'.format(
        inYoutubeId)
    requestObj = requests.get(url=requestUrl)

    # Match if video is not available/private/exists.
    if not requestObj.status_code != '200':
        return None

    if requestObj.text == 'Unauthorized':
        return None

    return requestObj.json()

def getVideoInfo(inYoutubeId,
                 inLanguageCode=None,
                 inCheckValidIdBool=True):

    videoBasicInfo = getVideoBasicInfo(inYoutubeId)

    if inCheckValidIdBool and not videoBasicInfo:
        return

    youtubeLink = 'https://www.youtube.com/watch?v={0}'.format(inYoutubeId)

    videoInfoDict = {'link': youtubeLink,
                     'title': videoBasicInfo['title'],
                     'id': inYoutubeId}

    if inLanguageCode:

        subtitleLanguages = getSubtitleLanguages(inYoutubeId)

        closestLanguage = getClosestLanguage(
            subtitleLanguages,
            inLanguageCode)

        if not closestLanguage:
            return

        videoInfoDict['subtitles'] = 'https://www.youtube.com/api/timedtext?lang={0}&v={1}'.format(
            closestLanguage,
            inYoutubeId)

    return videoInfoDict

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

            if inLanguageCode:
                getVideoInfoKwargs['inLanguageCode'] = inLanguageCode

            videoInfo = getVideoInfo(videoInfoDict['id'],
                                     inCheckValidIdBool=True,
                                     **getVideoInfoKwargs)

            if videoInfo:
                searchResults.append(videoInfo)

        retryCounter += 1
        ytSearch.next()

    return searchResults

'''
import time

videoInfo = getVideoInfo('omGF6Ps9Nog', 'es')

for x in range(10):
    t0 = time.time()
    getSubtitlesList(videoInfo['subtitles'])
    t1 = time.time()
    print(t1-t0)
    break
'''