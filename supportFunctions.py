import string,json,requests
from unidecode import unidecode

######################################################################################################

def cleanBand(bandName):
    '''
    Variable Fixing function- since the vagalume site uses a specific format to it's bands names this
    function was created to assure that format.
    '''
    all_normal_characters = string.ascii_letters + string.digits

    bandName = list(unidecode(str(bandName)))

    for i in range(0,len(bandName)):
        if bandName[i] not in all_normal_characters:
            if bandName[i].isspace() is True:
                bandName[i] = '-'
            elif bandName[i] == '.':
                bandName[i] = '-'
            else:
                bandName[i] = ''

    bandName = ''.join(bandName).lower()
    return bandName

###################################################################################################### 

def gSuggestion(bandName):
    '''
    Google suggestion function - uses the autocomplete API from google
    to guess the right name of the band in case of an unsucessefull crawl.
    '''    
    try:
        URL="http://suggestqueries.google.com/complete/search?client=chrome&q=" + bandName
                
        response=requests.get(URL)
                
        suggList = json.loads(response.content.decode('utf-8'))

        if len(suggList)>1:
            suggName = suggList[1][0]
            return suggName
    except:
        return None
