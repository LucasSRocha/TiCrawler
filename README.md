# TiCrawler
O TiCrawler foi criado para extrair listas de musicas, # top musicas do artista ou todas musicas associadas ao artista, de acordo com o  desejado pelo usuário. A busca é realizada no site www.vagalume.com.br e utiliza o modulo BeatifulSoup4 para realizar o parse do html extraido.

# Instalação  
git clone https://github.com/LucasSRocha/TiCrawler.git  
cd ../TiCrawler/  
pip3 install -r requiremets.txt  

# Utilização  
Para utilizar o script utiliza-se apenas o  arquivo 'TiCrawler.py'.  
O script pode ser utilizado a partir do nome direto da banda, utilizando o argumento -a, ou como o diretório de um arquivo .txt com o nome da banda(s) que deseja pesquisar, utilizando o argumento -p. É necessário definir um argumento para pesquisa de titulos no topo do artista, argumento -n número de titulos, ou de músicas do artista, argumento -as.  
Caso o nome do artista não seja encontrado no site será feita uma sugestão, cabendo ao usuário aceitar ou não.

<pre>
python TikalCrawler.py [-a/--as_argument 'ARTIST']<br/>
                       [-p/-band_file_path 'FILE_PATH']<br/>
                       [-n/--number "NUMBER OF TOP SONGS" Max=25, Default_value=25]<br/>
                       [-as/-all_songs <This argument will bring all musics related to the artist>]<br/>
                       [-h/--help <This argument will bring up this menu>]<br/>
</pre>

1. Retorno das 5 primeiras músicas no Top da banda Metallica
<pre>
python TiCrawler.py -a "Metallica" -n 5
Searching for Metallica...

1) Nothing Else Matters
2) Enter Sandman
3) The Unforgiven
4) One
5) Fade To Black

Would you like to save this list as a .txt file? (y/n)
n
</pre>
2. Retorno das 3 primeiras músicas no Top da banda 'Iron Maden'
<pre>
python TiCrawler.py -a "Iron Maden" -n 3

Sorry, couldn't find Iron Maden


Do you want to search for iron maiden instead and try again? (y/n)
y

Searching for iron maiden...

1) Fear Of The Dark
2) Wasting Love
3) The Number Of The Beast

Would you like to save this list as a .txt file? (y/n)
n
</pre>  
3. Retorno das 5 primeiras músicas no Top das bandas contidas no arquivo teste.txt
<pre>
teste.txt
  Iron Maiden
  Metallica
  Elton John
</pre>
<pre>
python TiCrawler.py -p teste.txt -n 5

Searching for Iron Maiden...

1) Fear Of The Dark
2) Wasting Love
3) The Number Of The Beast
4) The Trooper
5) Hallowed Be Thy Name

Would you like to save this list as a .txt file? (y/n)
n

Searching for Metallica...

1) Nothing Else Matters
2) Enter Sandman
3) The Unforgiven
4) One
5) Fade To Black

Would you like to save this list as a .txt file? (y/n)
n

Searching for Elton John...

1) Your Song
2) Skyline Pigeon
3) Sacrifice
4) Daniel
5) Nikita

Would you like to save this list as a .txt file? (y/n)
n
</pre>
