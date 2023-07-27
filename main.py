from bs4 import BeautifulSoup
import requests
import pathlib

url = 'https://loveworldlyrics.com/artiste/lyrics/'

articles = requests.get(url)
formattedOutput = BeautifulSoup(articles.text, 'lxml')
posts = formattedOutput.find_all('h2', class_='post-box-title')

for post in posts:
    postUrl = post.find('a', href=True)['href']

    singlePost = BeautifulSoup(requests.get(postUrl).text, 'lxml')
    songTitle = singlePost.find('h1', class_='name').span.string

    lyricsContainer = singlePost.find('div', class_='entry').find_all('p')
    lyrics = str(lyricsContainer).replace("<p>", "").replace(
        "</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br/>", "\n").replace("[", "").replace("]", "")

    print(lyrics)

    directory = pathlib.Path('./songs')
    with open(directory.joinpath(songTitle + ".txt"), 'w') as file:
        file.write(lyrics)


# Get the root url to scrape from
# On the songs page, songs are listed with their title and a short text
# Loop through all the articles on the root page and get the url for each and every article (song)
# On the page for specific articles(songs), look through the html and extract the title and the lyrics for the song
