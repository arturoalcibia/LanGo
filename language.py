import string

from constant import constants


def getLongLanguageName(inCode):
    '''

    Ex: en-GB
    '''
    inCodeSplit = inCode.split('-')

    if len(inCodeSplit) == 1:
        return constants.ISO_CODE_LANGUAGE_MAPPING.get(inCode, inCode)

    if len(inCodeSplit) == 2:
        return '-'.join( [constants.ISO_CODE_LANGUAGE_MAPPING.get(inCodeSplit [ 0], inCodeSplit[ 0]) ,
                          inCodeSplit[1]] )

    else:
        return inCode

def getShort(inCode):
    '''

    Ex: en-GB
    '''
    inCodeSplit = inCode.split('-')

    if len(inCodeSplit) == 1:
        return constants.ISO_CODE_LANGUAGE_MAPPING.get(inCode, inCode)

    if len(inCodeSplit) == 2:
        return '-'.join( [constants.ISO_CODE_LANGUAGE_MAPPING.get(inCodeSplit [ 0], inCodeSplit[ 0]) ,
                          inCodeSplit[1]] )

    else:
        return inCode

def stripPunctuation(inSentenceStr):
    return inSentenceStr.translate(str.maketrans('', '', string.punctuation))