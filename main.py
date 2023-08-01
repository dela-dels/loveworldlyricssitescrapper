from bs4 import BeautifulSoup
import requests
import pathlib

baseUrl = "https://loveworldlyrics.com/artiste/lyrics/"

response = requests.get(baseUrl)
formattedOutput = BeautifulSoup(response.text, "html.parser")

# The pagination html element holds the text as Page 1 of 60
# we want to split this text by spaces to get the page numbers (i.e 1 and 60)
splitPaginationELementText = formattedOutput.find(
    'span', class_='pages').get_text().split(" ")

firstPageNumber = int(splitPaginationELementText[1])

# We add 1 to the last page number because we will be using the range function to get a range of numbers
# to loop through. Caveat is that a call to this method, range(1, 60) will only loop to 59, not including the last number.
# Since we want to visit all the pages that exist, we will have to add 1 to the last page number to get the actual total number of pages
lastPageNumber = int(splitPaginationELementText[3]) + 1

for p in range(firstPageNumber, lastPageNumber):
    url = baseUrl + "page/" + str(p) + "/"

    print("visiting url to get lyrics: ", url)

    response = requests.get(url)
    output = BeautifulSoup(response.text, "html.parser")
    posts = output.find_all("h2", class_="post-box-title")

    for post in posts:
        postUrl = post.find("a", href=True)["href"]

        # singlePost = BeautifulSoup(requests.get(postUrl).text, 'html.parser')
        singlePost = BeautifulSoup(
            requests.get(postUrl).text, "html.parser")
        songTitle = singlePost.find("h1", class_="name").span.string

        """
        While crawling through a single post for lyrics, there is a series of anchor tags that look like this:
        <a data-type="URL">Written by Simeon</a> or  <a class="wp-block-button__link">some random wordpress link</a> Since we wouldn't be needing this
        and it'll making importing lyrics into the projection software easier, we strip out all occurrences of an <a></a> tag. with these attributes
        """
        # TODO: check to see if these elements actually exist before removing them to saving resources
        for a in singlePost.find_all("a", attrs={"class": "wp-block-button__link"}):
            a.decompose()

        for a in singlePost.find_all("a", attrs={"data-type": "URL"}):
            a.decompose()

        directory = pathlib.Path("./songs")
        print("filename: ", songTitle.replace("-", " ")+".txt")
        filename = songTitle.replace(
            "-", " ").replace("/", " ").replace("|", " ") + ".txt"
        with open(directory.joinpath(filename), 'a') as file:
            for t in singlePost.find("div", class_="entry").find_all("p"):
                file.write(t.get_text() + "\n")
