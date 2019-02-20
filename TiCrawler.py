import argparse
from support_module import TcrawlTech


def main():
    parser = argparse.ArgumentParser(
        prog="TiCrawler - Vagalume Crawler",
        usage="""python TikalCrawler.py [-a/--as_argument 'ARTIST']
                              [-p/-band_file_path 'FILE_PATH']
                              [-n/--number "NUMBER OF TOP SONGS" Max=25, Default_value=25]
                              [-as/-all_songs <This argument will bring all musics related to the artist>]
                              [-h/--help <This argument will bring up this menu>]

Exemplas of usage:

-Get n top songs:
    python TiCrawler.py -a "Metallica" -n 3
        output: '1) Nothing Else Matters
                 2) Enter Sandman
                 3) The Unforgiven'

    python TiCrawler.py -p 'C://Bands.txt' -n 1
	    where: Bands.txt contains:
             'Iron Maiden
              Metallica
              Elton John'
        output: '1)Fear of The Dark

                 1)Nothing Else Matters	

                 1)Your Song'

-Get all songs related to artist:
    python TiCrawler.py -a "Metallica" -as
       			
    python TiCrawler.py -p 'C://Bands.txt' -as""",
        description="A python script to search and show songs from a related artist",
    )
    parser.add_argument(
        "artist",
        type=str,
        help='"Artist" or path of .txt file containing artist to be searched',
    )
    groupInput = parser.add_mutually_exclusive_group()
    groupInput.add_argument(
        "-p",
        "--band_file_path",
        action="store_true",
        default=False,
        help="To set the name of the artist from a .txt in the local path",
    )
    groupInput.add_argument(
        "-a",
        "--as_argument",
        action="store_true",
        default=False,
        help="To set the name of the artist as a argument",
    )

    groupChoice = parser.add_mutually_exclusive_group()
    groupChoice.add_argument(
        "-n",
        "--number",
        type=int,
        default=25,
        help="Number of top songs to be extracted, 25 beeing the max",
    )
    groupChoice.add_argument(
        "-as",
        "--all_songs",
        action="store_true",
        default=False,
        help="Extract all songs from your selected artist",
    )

    args = parser.parse_args()

    if args.band_file_path:
        # read all the lines from the band_file_path in case theres more than one band
        band_file_path = open(args.artist, "r")
        lines_list = band_file_path.readlines()
        band_file_path.close()

        for i in range(0, len(lines_list)):
            lines_list[i] = str(lines_list[i].replace("\n", ""))

        for j in lines_list:
            if args.all_songs:

                crawler = TcrawlTech(j)
                res = crawler.search_all_songs(crawler.vagalume_connect())

                if res is True:
                    save = str(
                        input(
                            "\nWould you like to save this list as a .txt file? (y/n)\n"
                        )
                    ).lower()

                    if save in ["y", "yes", "sim"]:
                        crawler.save_crawl()
            else:
                crawler = TcrawlTech(j, args.number)

                res = crawler.top_list(crawler.vagalume_connect())

                if res is True:
                    save = str(
                        input(
                            "\nWould you like to save this list as a .txt file? (y/n)\n"
                        )
                    ).lower()

                    if save in ["y", "yes", "sim"]:
                        crawler.save_crawl()
    if args.as_argument:
        if args.all_songs:
            crawler = TcrawlTech(args.artist)

            res = crawler.search_all_songs(crawler.vagalume_connect())

            if res is True:
                save = str(
                    input("\nWould you like to save this list as a .txt file? (y/n)\n")
                ).lower()

                if save in ["y", "yes", "sim"]:
                    crawler.save_crawl()
        else:
            crawler = TcrawlTech(args.artist, args.number)

            res = crawler.top_list(crawler.vagalume_connect())

            if res is True:
                save = str(
                    input("\nWould you like to save this list as a .txt file? (y/n)\n")
                ).lower()

                if save in ["y", "yes", "sim"]:
                    crawler.save_crawl()


if __name__ == "__main__":
    main()
