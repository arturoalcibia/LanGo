def loadEnglishToList():

    words = 'words = ('

    for fileObj in [ open('./english1000', 'r') ,
                     open('./english2000', 'r') ]:

        for index, lineStr in enumerate(fileObj.readlines()):

            if '[[' not in lineStr:
                continue

            word = lineStr.split('[[')[1].split(']]')[0].lower()
            word = word.replace('\'', "\\'")
            words += '\'{0}\',\n'.format(word)

    words += ')'

    with open('../constant/english.py', 'w') as f:
        f.write(words)

def loadSpanishToList():

    wordsSet = []

    for filePath in ['./spanish1000' ,
                     './spanish2000' ]:

        with open(filePath, 'r', encoding='UTF-8') as fileObj:

            for index, lineStr in enumerate(fileObj.readlines()):

                if '[[' not in lineStr:
                    continue

                if 'wik' in lineStr.lower():
                    continue

                word = lineStr.split('[[')[1].split('#')[0].lower()

                if word in wordsSet:
                    continue

                wordsSet.append(word)

    words = 'words = ('
    for word in wordsSet:
        words += '\'{0}\',\n'.format(word)
    words += ')'

    with open('../constant/spanish.py', 'w', encoding='UTF-8') as f:
        f.write(words)


def loadFrenchToList():

    wordsSet = []

    for filePath in ['./french5000' ]:

        with open(filePath, 'r', encoding='UTF-8') as fileObj:

            for index, lineStr in enumerate(fileObj.readlines()):

                if '[[' not in lineStr:
                    continue

                if 'wik' in lineStr.lower():
                    continue

                word = lineStr.split('}}')[-1].split('|')[-1].lower()

                if word in wordsSet:
                    continue

                wordsSet.append(word)

    words = 'words = ('
    for word in wordsSet:
        words += '\'{0}\',\n'.format(word)
    words += ')'

    with open('../constant/french.py', 'w', encoding='UTF-8') as f:
        f.write(words)


if __name__ == "__main__":
    #loadEnglishToList()
    #loadSpanishToList()
    loadFrenchToList()