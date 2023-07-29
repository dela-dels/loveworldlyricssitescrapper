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

    """
    While crawling through a single post for lyrics, there is a series of anchor tags that look like this:
    <a data-id="2528" data-type="post" data-id="https://loveworldlyrics.com/artiste/simeon-rich/" data-type="URL"
    href="https://loveworldlyrics.com/artiste/simeon-rich/">Written by Simeon</a>. Since we wouldn't be needing this
    and it'll making importing lyrics into the projection software easier, we strip out all occurrences of an <a></a> tag.
    """
    for a in singlePost.find_all('a'):
        a.decompose()

    lyricsContainer = singlePost.find('div', class_='entry').find_all('p')

    lyrics = str(lyricsContainer).replace("<p>", "").replace(
        "</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br/>", "\n").replace("[", "").replace("]", "")
    print(lyrics)

    directory = pathlib.Path('./songs')
    with open(directory.joinpath(songTitle + ".txt"), 'w') as file:
        file.write(lyrics)


# Get the root url to scrape from
# On the songs page, songs are listed with their title and a short text
# Loop through all the articles on the root page and get the url for each and every article (song) NB: This is a paginated list
# On the page for specific articles(songs), look through the html and extract the title and the lyrics for the song
