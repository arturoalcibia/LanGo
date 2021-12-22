import constant.spanish
from constant import constants


def splitSentence(inSentence):
    '''Splits a sentence by words. Adds a key if each word should be displayed or shown as blank
    if found on the dictionary.

    Args:
         inSentence (str): sentence str.

    Returns:
        list[ list [ str  , # word(s).
                     bool ] # bool value, True if displayed as blank
                            ]
    '''

    # List with a portion of the sentence as index 0
    # and true if hint, false if blank as index 1.
    # type: list[list[str, bool]]
    wordTuples = []

    # List to be used as an index to slice the sentence.
    # type: list[int]
    wordIndices = []

    splittedSentence = inSentence.split(' ')

    # Define if word will be a hint or blank.
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