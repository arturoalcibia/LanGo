import bisect
import collections
import requests
import urllib.request
import xml.etree.ElementTree

import youtube_dl
from youtubesearchpython import *

import constants

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
    with urllib.request.urlopen(inSubtitlesUrl) as response:
        subsXml = xml.etree.ElementTree.parse(response)
        subRoot = subsXml.getroot()
        subs = []
        for xmlElement in subRoot:
            start = xmlElement.attrib['start']

            # Used to precise display
            startFloat = float(start)

            subs.append({'end': round(float(xmlElement.attrib['dur']) + startFloat, 2),
                         'start': startFloat,
                         'text': xmlElement.text})

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

