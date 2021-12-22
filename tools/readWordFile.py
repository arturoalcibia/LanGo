# move to tools
file1 = open('../constant/spanish.txt', 'r', encoding="utf-8")
for index, txt in enumerate(file1.readlines()):

    txt = txt.strip().split(' ')[0]

    if index == 0:
        print(' words = set( \'{0}\' ,'.format(txt))

    elif index + 1 == len(file1.readlines()):
        print('\'{0}\' )'.format(txt))

    else:
        print('\'{0}\' ,'.format(txt))

    if index > 50000:
        break