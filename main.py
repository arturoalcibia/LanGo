# todo! request subtitles flag on youtube_dl

import time
import os
import re
import shutil
import threading
import urllib.request

import xml.etree.ElementTree

import youtube_dl

from youtubesearchpython import *

ALPHANUM_RE = re.compile('[^a-zA-Z]')

def splitTrack(inFile,
               inDestFolder,
               inStart,
               inEnd):

    destFile = os.path.join(inDestFolder, '{0}_{1}.m4a'.format(inStart, inEnd))

    os.system(
        'ffmpeg -i {sourceFile} '
        '-ss {subStart} '
        '-to {subEnd} '
        '-c copy "{destFile}"'.format(
            sourceFile=inFile,
            destFile=destFile,
            subStart=inStart,
            subEnd=inEnd)
    )

def main(inVideoUrlStr):



    queryOptsDict = {
        'extractaudio': True,
        'format': 'worstaudio',
        'quiet':True
    }

    # todo! add a check if no subtitles
    with youtube_dl.YoutubeDL(queryOptsDict) as ydl:
        videoInfo = ydl.extract_info(
            inVideoUrlStr,
            download=False)

    songTitle = videoInfo["title"]
    alpNumSongTitle = ALPHANUM_RE.sub('', songTitle)
    ext       = videoInfo["ext"]
    fileName  = '{0}.{1}'.format(alpNumSongTitle, ext)

    subtitles = videoInfo.get('subtitles', {})
    print(subtitles.keys())

    return

    downloadOptsDict = {
        'extractaudio': True,
        'format'      : 'worstaudio',
        'outtmpl'     : fileName}

    with youtube_dl.YoutubeDL(downloadOptsDict) as ydl:
        ydl.extract_info(
            inVideoUrlStr,
            download=True)

    # todo! add a check if file does not exist.
    tracksDir = 'audioTracks'
    if os.path.exists(tracksDir):
        shutil.rmtree(tracksDir)

    os.mkdir(tracksDir)
    fileNamePath = os.path.join(os.getcwd(), fileName)

    subtitles = videoInfo.get('subtitles')

    validSubtitleFormats = ('srv1', 'srv2', 'srv3')



    for lang, subList in subtitles.items():

        for subDict in subList:

            if subDict.get('ext') in validSubtitleFormats:
                subLink = subDict.get('url')

                # todo! proper structure/ urllib can be replaced with requests.get ?
                with urllib.request.urlopen(subLink) as response:
                    subsXml = xml.etree.ElementTree.parse(response)

                break

    root = subsXml.getroot()

    subInfo = []

    for child in root:
        subStart = float(child.attrib['start'])
        subEnd = subStart + float(child.attrib['dur'])
        subText = child.text

        #subStart = round(subStart - 1, 2)
        #subEnd   = round(subEnd + 1, 2)

        subInfo.append((subStart, subEnd))

    threads = []
    '''
    for subStart, subEnd in subInfo:
        splitTrack(fileNamePath, tracksDir, subStart, subEnd)
    '''
    for index, (subStart, subEnd) in enumerate(subInfo):

        threads.append(
            threading.Thread(
                target=splitTrack,
                args=(fileNamePath,
                      tracksDir,
                      subStart,
                      subEnd)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


start = time.time()

videosSearch =  CustomSearch('francais', 'EgYYAygBMAE%253D', limit = 100, language = 'fr')

for x in videosSearch.result()['result']:
    print('#' * 80)
    print(x['title'])
    main(x['link'])
    print('#' * 80)

end = time.time()
print(end - start)