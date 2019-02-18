import requests
from bs4 import BeautifulSoup
from supportFunctions import cleanBand, gSuggestion

class TcrawlT:
    '''
    class that stores the crawling functions to be used in www.vagalume.com.br
    it has:
    -bandName - which artist the crawl will try to lookup
    -ntop     - how many musics from the top 25 will be crawled
    '''

######################################################################################################  
    
    def __init__(self, bandName, ntop = 25):
        self.bandName = bandName        #Name of the artist
        self.ntop = ntop                #Number of top songs to extract
        self.listSongs = list()         #List to be used as output
        


###################################################################################################### 

    def conn(self):
        
        #Function to connect to the vagalume site - URL + bandName - and extract all the html information
        
        baseUrl = 'https://www.vagalume.com.br/'

        targetSite = requests.get(baseUrl + cleanBand(self.bandName))
        
        urlSoup = BeautifulSoup(targetSite.text,'lxml')

        if urlSoup.find('div',class_='errorContentBg') is not None:

          #Wrong bandName couldnt find at vagalume -> Make suggestion if possible
          
          print("Sorry, couldn't find " + self.bandName +'\n')
          
          bandName = gSuggestion(self.bandName)
          
          if bandName is None:
                print("Couldn't find a suggestion for your query")
          else:
              suggResponse = str(input("Do you want to search for "+ bandName + " instead and try again? (y/n)\n")).lower()
    
              if suggResponse in ['y','yes','sim']:
                     
                  targetSite = requests.get("https://www.vagalume.com.br/" + cleanBand(bandName))

                  urlSoup = BeautifulSoup(targetSite.text,"lxml")
                  
                  if urlSoup.find('div',class_='errorContentBg') is not None:

                      print("Well that didn't work as well...please check your connection and the artist name that you're trying to crawl")
        return urlSoup
                      
###################################################################################################### 

    def topList(self,htmlSoup):
        #find the n top musics by the html tag using the html information gathered from the conn() function 
        if htmlSoup.find('div',class_='errorContentBg') is None:
            for i in range(0,self.ntop):
                self.listSongs.append(htmlSoup.find('ol',id='topMusicList').find_all('a',class_='nameMusic')[i].text)
            self.listSongs = '\n'.join(self.listSongs)
            print(self.listSongs)
            return True
            
######################################################################################################

    def fullSongs(self,htmlSoup):
        #find all the musics by the html tag using the html information gathered from the conn() function 
        if htmlSoup.find('div',class_='errorContentBg') is None:
            for i in htmlSoup.find('ol',id='alfabetMusicList').find_all('a',class_='nameMusic'):
                self.listSongs.append(i.text)
            self.listSongs = '\n'.join(self.listSongs)
            print(self.listSongs)
            return True



######################################################################################################

    def saveCrawl(self):
        #saves a local file at the source location with the name of the Band
        file = open(self.bandName+'.txt','w')
        file.write(self.listSongs)
        file.close()
        
