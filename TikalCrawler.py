import argparse
from Tcrawl import TcrawlT

def main():
    parser = argparse.ArgumentParser(prog='Web Crawler',
                                     usage=''''python TikalCrawler.py "artist/path" -f [search artist from file] -a [search artist from argument] -n [n top songs from selected artist] -as [all songs from selected artist]''',
                                     description='Main focus of this program is to output the top 25 musics from a selected artist')
    parser.add_argument('artist',type=str, help = '"Artist" or path of .txt file containing artist to be searched')
    groupInput = parser.add_mutually_exclusive_group()
    groupInput.add_argument('-f','--file', action='store_true',default=False, help = 'To load the name of the artist from a local .txt file')
    groupInput.add_argument('-a','--argument', action='store_true',default=False, help='To load the name of the artist as a argument')   

    groupChoice = parser.add_mutually_exclusive_group()
    groupChoice.add_argument('-n','--number', type=int,default=25,help='Number of top songs to be extracted, 25 beeing the max')
    groupChoice.add_argument('-as','--allSongs', action='store_true',default=False,help = 'Extract all songs from your selected artist') 

    args = parser.parse_args()

    if args.file:
        #read all the lines from the file in case theres more than one band
        file = open(args.artist,'r')
        linesList = file.readlines()
        file.close()
        
        for i in range(0,len(linesList)):
            linesList[i]=str(linesList[i].replace('\n',''))
           
        for j in linesList:
            if args.allSongs:
                crawler = TcrawlT(j)
                
                res = crawler.fullSongs(crawler.conn())
                
                if res is True:
                    save = str(input('\nWould you like to save this list as a .txt file? (y/n)\n')).lower()
                               
                    if save in ['y','yes','sim']:
                        crawler.saveCrawl()
            else:
                crawler = TcrawlT(j,args.number)
                
                res = crawler.topList(crawler.conn())
                
                if res is True:
                    save = str(input('\nWould you like to save this list as a .txt file? (y/n)\n')).lower()
                               
                    if save in ['y','yes','sim']:
                        crawler.saveCrawl()
    if args.argument:
            if args.allSongs:
                crawler = TcrawlT(args.artist)
                
                res = crawler.fullSongs(crawler.conn())
                
                if res is True:
                    save = str(input('\nWould you like to save this list as a .txt file? (y/n)\n')).lower()
                               
                    if save in ['y','yes','sim']:
                        crawler.saveCrawl()
            else:
                crawler = TcrawlT(args.artist,args.number)
                
                res = crawler.topList(crawler.conn())
                
                if res is True:
                    save = str(input('\nWould you like to save this list as a .txt file? (y/n)\n')).lower()
                               
                    if save in ['y','yes','sim']:
                        crawler.saveCrawl()        
        



if __name__ == '__main__':
    main()
