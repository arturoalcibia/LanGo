if __name__ == "__main__":

    import time
    import urllib.request
    import xml.etree.ElementTree

    import youtube

    import constants

    def isValidWord(inWordStr):

        if len(inWordStr) == 2:
            return False

        return True

    videoInfo = youtube.getVideoInfo('bFrtwXpbR9s',
                                    constants.LANGUAGE_ISO_CODE_MAPPING['English'])

    subtitles = videoInfo['subtitles']

    with urllib.request.urlopen(videoInfo['subtitles']) as response:
       subsXml = xml.etree.ElementTree.parse(response)
       root = subsXml.getroot()


    start = time.time()
    # Note: Skip print statements to truly assess time functions.
    for xmlElement in root:
        text= xmlElement.text# Your function goes here
        print(isValidWord(text))
    end = time.time()
    print(end - start)