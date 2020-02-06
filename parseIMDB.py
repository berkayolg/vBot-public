import requests, random
from bs4 import BeautifulSoup

class Movie:
    def __init__(self, order, title, year, rating, url, image):
        self.order = order
        self.title = title
        self.year = year
        self.rating = rating
        self.url = url
        self.image = image

    def __str__(self):
        return ' '.join([self.order, self.title, self.year, self.rating])
    
    def caption(self):
        return ' '.join([self.title, '\n', self.url])

def movieGenres():
    return ['action','adventure','animation','biography','comedy',
    'crime','drama','family','fantasy','film_noir',
    'history','horror','music','musical','mystery',
    'romance','sci_fi','sport','thriller','war','western']

def showGenres():
    return ['action','adventure','animation','biography','comedy',
    'crime','documentary','drama','family','fantasy','game_show',
    'history','horror','music','musical','mystery','news','reality_tv',
    'romance','sci_fi','short','sport','talk_show','thriller','war','western']

#Parses rows and turn them into movie objects
def rowParser(row):
    meta = str(row.text).split()
    r = requests.get('https://www.imdb.com' + row.a['href'])
    soup = BeautifulSoup(r.content, features='html.parser')
    imageURL = soup.find("div", {"class":"poster"}).img['src']
    return Movie(meta[0], ' '.join(map(str,meta[1:-7])), meta[-7], meta[-6], 'https://www.imdb.com' + row.a['href'] , imageURL)

#Takes tv shows from the top 250, returns them as a list
def initShows():
    print('Initializing the show records.')
    r = requests.get('https://www.imdb.com/chart/toptv/')
    soup = BeautifulSoup(r.content, features='html.parser')
    rows = soup.find_all('tr')
    showList = list()
    for row in rows[1:251]:
        showList.append(rowParser(row))
    return showList

#Takes movies from the top 250, returns them as a list
def initMovies():
    print('Initializing the movie records.')
    r = requests.get('https://www.imdb.com/chart/top')
    soup = BeautifulSoup(r.content, features='html.parser')
    rows = soup.find_all('tr')
    movieList = list()
    for row in rows[1:251]:
        movieList.append(rowParser(row))
    return movieList

#URL generators for any specific genre
def urlShowGenre(genre):
    return '''https://www.imdb.com/search/title/?genres=%s&sort=user_rating,
    desc&title_type=tv_series,mini_series&num_votes=5000,&pf_rd_m=A2FGELUUNOQJNL&
    pf_rd_p=f85d9bf4-1542-48d1-a7f9-48ac82dd85e7&pf_rd_r=7429MADT9GGRAVXMRVA9&pf_
    rd_s=right-6&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_gnr_1'''%genre

def urlMovieGenre(genre):
    return '''https://www.imdb.com/search/title/?genres=%s&sort=user_rating,de
    sc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f
    -35eb-40f3-95f7-c53f09d542c3&pf_rd_r=DEVV4A6GBEK1TEQT9TBD&pf_rd_s=right-6&pf_r
    d_t=15506&pf_rd_i=top&ref_=chttp_gnr_1'''%genre

def getShowGenreList(genre):
    #Open the genre section
    url = urlShowGenre(genre)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')

    #Taking every list item, list items include title, rating and year information
    showsList = list()
    rows = soup.find_all("h3", attrs={"class":"lister-item-header"})
    ratings = soup.find_all("div", attrs={"class":"inline-block ratings-imdb-rating"})
    images = soup.find_all("div", attrs={"class":"lister-item-image float-left"})
    i = 0
    for row in rows:
        #Large size images are taken from the main sites of the shows and movies
        r = requests.get('https://www.imdb.com' + row.a['href'])
        soup = BeautifulSoup(r.content, features='html.parser')
        imageURL = soup.find("div", {"class":"poster"}).img['src']

        year = row.find('span', attrs={'class':'lister-item-year text-muted unbold'}).text
        address = 'https://www.imdb.com' + images[i].a['href']
        show = Movie(str(i+1)+'.', row.a.text, year, ratings[i].strong.text, address, imageURL)
        i += 1
        showsList.append(show)
    return showsList

def getMovieGenreList(genre):
    #Open the genre section
    url = urlMovieGenre(genre)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')

    #Taking every list item, list items include title, rating and year information
    moviesList = list()
    rows = soup.find_all("h3", attrs={"class":"lister-item-header"})
    ratings = soup.find_all("div", attrs={"class":"inline-block ratings-imdb-rating"})
    images = soup.find_all("div", attrs={"class":"lister-item-image float-left"})
    i = 0
    for row in rows:
        #Large size images are taken from the main sites of the shows and movies
        r = requests.get('https://www.imdb.com' + row.a['href'])
        soup = BeautifulSoup(r.content, features='html.parser')
        imageURL = soup.find("div", {"class":"poster"}).img['src']

        year = row.find('span', attrs={'class':'lister-item-year text-muted unbold'}).text
        address = 'https://www.imdb.com' + images[i].a['href']
        movie = Movie(str(i+1)+'.', row.a.text, year, ratings[i].strong.text, address, imageURL)
        i += 1
        moviesList.append(movie)
    return moviesList

#Initialize show genres dictionary
def initShowGenres():
    genres = showGenres()

    print('Initializing the genre records for top tv shows.')
    showGenresDict = dict()
    for genre in genres:
        genreList = getShowGenreList(genre)
        showGenresDict[genre] = genreList
    return showGenresDict

#Initialize movie genres dictionary
def initMovieGenres():
    genres = movieGenres()

    print('Initializing the genre records for top movies.')
    movieGenresDict = dict()
    for genre in genres:
        genreList = getMovieGenreList(genre)
        movieGenresDict[genre] = genreList
    return movieGenresDict

#Get random row record from a file
def getRandRecord(filePath):
    file = open(filePath, 'r')
    #Number of lines in a file
    fLen = len(file.readlines(  ))
    file.seek(0)
    
    i = 0
    randI = random.randint(0,fLen-1)
    for line in file:
        if i == randI:
            meta = line.split()
            movie = Movie(meta[0], ' '.join(map(str,meta[1:-3])), meta[-3], meta[-2], meta[-1], meta[-1])
            print(movie.url)
            return movie
        i += 1
    file.close()
   
#Wrapper function for getting random record from files
def getRand(movieFlag = False, showFlag = False, genre=None):
    #If no genre specified, get record from top 250
    if genre == []:
        if movieFlag is True:
            return getRandRecord('./data/movies.txt')
        else:
            return getRandRecord('./data/shows.txt')
    #Take record from specified genre file
    else:
        if movieFlag is True:
            return getRandRecord('./data/movie_' + genre[0] + '.txt')
        else:
            return getRandRecord('./data/show_' + genre[0] + '.txt')

#Writing the records from imdb to files.
def writeRecords(movieList, showList, showGenresDict, movieGenresDict):
    showGenres = showGenres()

    movieGenres = movieGenres()

    #For top 250 movies.
    movieFile = open('./data/movies.txt', 'w')
    for movie in movieList:
        movieFile.write(str(movie)+'\n')
    movieFile.close()

    #For top 250 tv shows.
    showFile = open('./data/shows.txt', 'w')
    for show in showList:
        showFile.write(str(show)+'\n')
    showFile.close()

    #For specific genres of shows all from top 50 lists.
    for genre in showGenres:
        fGenre = open('./data/show_'+genre+'.txt', 'w')
        for show in showGenresDict[genre]:
            fGenre.write(str(show)+'\n')
        fGenre.close()
     
    for genre in movieGenres:
        fGenre = open('./data/movie_'+genre+'.txt', 'w')
        for show in movieGenresDict[genre]:
            fGenre.write(str(show)+'\n')
        fGenre.close()