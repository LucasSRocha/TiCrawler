import json #to parse result from google_suggestion function
import string #used to bring all acceptable characters for variable threatment
import requests #used to request vagalume html page
from bs4 import BeautifulSoup #html parser using 'lxml'
from unidecode import unidecode #used to replace special characters in usr_band_name 

######################################################################################################

def clean_band(band_name):
    """
    Variable Fixing function- since the vagalume site uses a specific format to it's bands names this
    function was created to assure that format.

    
    i.e:
    Yes: lowercase, no space, no special characters(except '-')
        "iron-maiden"
        "metallica"
        "elton-john"
        "system-of-a-down"

    No: uppercase, spaces and specials characters
        "Iron Maiden"
        "Metallica"
        "ElToN JoHn"
        " s y s t e m o f a d o w n " 


        Args: 
            band_name: string
    """

    #list of acceptable characters for comparison with band_name given to function
    all_normal_characters = string.ascii_letters + string.digits

    band_name = list(unidecode(str(band_name)))

    for i in range(0, len(band_name)):

        if band_name[i] not in all_normal_characters:

            if band_name[i].isspace() is True:

                band_name[i] = "-"

            elif band_name[i] == ".":

                band_name[i] = "-"

            else:

                band_name[i] = ""

    band_name = "".join(band_name).lower()

    return band_name


######################################################################################################


def google_suggestion(band_name):
    """
    Google suggestion function - uses the autocomplete API from google
    to guess the right name of the band in case of an unsucessefull crawl.
    
    i.e:
    input: "Eltun Jon"
    output: "Elton John"

    input:    "Iron Maden"
    output: "Iron Maiden"

    Args:
        band_name: string
    """

    try:
        google_suggestion_url = (
            "http://suggestqueries.google.com/complete/search?client=chrome&q="
            + band_name
        )

        url_response = requests.get(google_suggestion_url)

        suggestion_list = json.loads(url_response.content.decode("utf-8"))

        if len(suggestion_list) > 1:
            suggestion_band_name = suggestion_list[1][0]
            return suggestion_band_name
    except:
        return None


class TcrawlTech:
    """
    class that stores the crawling functions to be used in www.vagalume.com.br
    it has:
    -usr_band_name - which is the artist the crawl will try to lookup
    -number_top_songs - how many musics from the top 25 will be crawled
    -crawled_songs_list - list to store the results from the crawl
    """

    ######################################################################################################

    def __init__(self, usr_band_name, number_top_songs=25):
        self.usr_band_name = usr_band_name  # Name of the artist
        self.number_top_songs = number_top_songs  # Number of top songs to extract
        self.crawled_songs_list = list()  # List to be used as output

    ######################################################################################################

    def vagalume_connect(self):
        """
        # Function to connect to the vagalume site - URL + usr_band_name - and extract the html information
    """
        vagalume_url = "https://www.vagalume.com.br/"

        # clean_band is used to ensure proper utilization of the variable in the site
        vagalume_complete_url = requests.get(
            vagalume_url + clean_band(self.usr_band_name)
        )

        url_soup = BeautifulSoup(vagalume_complete_url.text, "lxml")

        # If the user defined band_name wasn't found at the vagalume site it
        # triggers google_suggestion function and offer the user a new
        # band_name

        if url_soup.find("div", class_="errorContentBg") is not None:

            print("\nSorry, couldn't find " + self.usr_band_name + "\n")

            google_suggestion_name = google_suggestion(self.usr_band_name)

            if google_suggestion_name is None:
                print("\nCouldn't find a suggestion for your query\n")
            else:
                usr_suggestion_response = str(
                    input(
                        "\nDo you want to search for "
                        + google_suggestion_name
                        + " instead and try again? (y/n)\n"
                    )
                ).lower()

                if usr_suggestion_response in ["y", "yes", "sim"]:
                    self.usr_band_name = google_suggestion_name

                    vagalume_complete_url = requests.get("https://www.vagalume.com.br/" + clean_band(google_suggestion_name))

                    url_soup = BeautifulSoup(vagalume_complete_url.text, "lxml")

                    if url_soup.find("div", class_="errorContentBg") is not None:

                        print(
                            "\nWell that didn't work as well...please check your connection and the artist name that you're trying to crawl\n"
                        )
        return url_soup

    ######################################################################################################

    def top_list(self, html_soup):
        """
        Find the class defined quantity of top musics by the html tag using the html information gathered from the vagalume_connect() function
        """
        
        if html_soup.find("div", class_="errorContentBg") is None:

            print("\nSearching for " + self.usr_band_name + "...\n")
            
            for i in range(0, self.number_top_songs):
                self.crawled_songs_list.append(str(i+1)+ ") " + html_soup.find("ol", id="topMusicList").find_all("a", class_="nameMusic")[i].text)

            self.crawled_songs_list = "\n".join(self.crawled_songs_list)

            print(self.crawled_songs_list)

            return True

    ######################################################################################################

    def search_all_songs(self, html_soup):
        """
        Find all songs releated to artist by specified tag used at vagalume html.

        Args:
        html_soup: html content returned from function vagalume_connect()
        """
        if html_soup.find("div", class_="errorContentBg") is None:
            print("\nSearching for " + self.usr_band_name + "...\n")
            for i in html_soup.find("ol", id="alfabetMusicList").find_all("a", class_="nameMusic"):
                self.crawled_songs_list.append(i.text)
            self.crawled_songs_list = "\n".join(self.crawled_songs_list)
            print(self.crawled_songs_list)
            return True

    ######################################################################################################

    def save_crawl(self):
        # saves a local file at the source location with the name of the Band
        file = open(self.usr_band_name + ".txt", "w")

        file.write(self.crawled_songs_list)

        file.close()
