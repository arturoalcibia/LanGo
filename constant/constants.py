# Number of videos to display when browsing.
SEARCH_LIMIT = 1

# Number of videos to dislay on the reccomendations page.
RECCOMMENDATIONS_LIMIT = 5

# Number of times to retry a query if no videos are found.
RETRY_LIMIT = 1

# Long name of language as key
# and language code as extracted from youtube-dl subtitles as value.
# Extracted from: https://www.andiamo.co.uk/resources/iso-language-codes/
LANGUAGE_ISO_CODE_MAPPING = {
'Afrikaans'	:'af',
'Albanian'	:'sq',
'Arabic'	:'ar',
'Basque'	:'eu',
'Belarusian'	:'be',
'Bulgarian'	:'bg',
'Catalan'	:'ca',
'Chinese'	:'zh',
'Croatian'	:'hr',
'Czech'	:'cs',
'Danish'	:'da',
'Dutch'	:'nl',
'English'	:'en',
'Estonian'	:'et',
'Faeroese'	:'fo',
'Farsi'	:'fa',
'Finnish'	:'fi',
'French'	:'fr',
'Gaelic'	:'gd',
'German'	:'de',
'Greek'	:'el',
'Hebrew'	:'he',
'Hindi'	:'hi',
'Hungarian'	:'hu',
'Icelandic'	:'is',
'Indonesian'	:'id',
'Irish'	:'ga',
'Italian'	:'it',
'Japanese'	:'ja',
'Korean'	:'ko',
'Kurdish'	:'ku',
'Latvian'	:'lv',
'Lithuanian'	:'lt',
'Macedonian'	:'mk',
'Malayalam'	:'ml',
'Malaysian'	:'ms',
'Maltese'	:'mt',
'Norwegian'	:'no',
'Polish'	:'pl',
'Portuguese'	:'pt',
'Punjabi'	:'pa',
'Rhaeto-Romanic'	:'rm',
'Romanian'	:'ro',
'Russian'	:'ru',
'Serbian'	:'sr',
'Slovak'	:'sk',
'Slovenian'	:'sl',
'Sorbian'	:'sb',
'Spanish'	:'es',
'Swedish'	:'sv',
'Thai'	:'th',
'Tsonga'	:'ts',
'Tswana'	:'tn',
'Turkish'	:'tr',
'Ukrainian'	:'uk',
'Urdu'	:'ur',
'Venda'	:'ve',
'Vietnamese'	:'vi',
'Welsh'	:'cy',
'Xhosa'	:'xh',
'Yiddish'	:'ji',
'Zulu'	:'zu'
}

ISO_CODE_LANGUAGE_MAPPING = {value : key for (key, value) in LANGUAGE_ISO_CODE_MAPPING.items()}
