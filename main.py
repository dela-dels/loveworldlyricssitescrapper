from bs4 import BeautifulSoup
import requests
import pathlib

url = 'https://loveworldlyrics.com/artiste/lyrics/'

response = requests.get(url)
# formattedOutput = BeautifulSoup(response.content, 'html.parser')
formattedOutput = BeautifulSoup(response.text, 'html.parser')
posts = formattedOutput.find_all('h2', class_='post-box-title')

for post in posts:
    postUrl = post.find('a', href=True)['href']

    # singlePost = BeautifulSoup(requests.get(postUrl).content, 'html.parser')
    singlePost = BeautifulSoup(requests.get(postUrl).content, 'lxml')
    songTitle = singlePost.find('h1', class_='name').span.string

    """
    While crawling through a single post for lyrics, there is a series of anchor tags that look like this:
    <a data-id="2528" data-type="post" data-id="https://loveworldlyrics.com/artiste/simeon-rich/" data-type="URL"
    href="https://loveworldlyrics.com/artiste/simeon-rich/">Written by Simeon</a>. Since we wouldn't be needing this
    and it'll making importing lyrics into the projection software easier, we strip out all occurrences of an <a></a> tag.
    """
    for a in singlePost.find_all('a', attrs={"class": "wp-block-button__link"}):
        a.decompose()

    for a in singlePost.find_all('a', attrs={"data-type": "URL"}):
        a.decompose()

    directory = pathlib.Path('./songs')
    with open(directory.joinpath(songTitle + ".txt"), 'a') as file:
        for t in singlePost.find('div', class_='entry').find_all('p'):
            file.write(t.get_text() + "\n")
