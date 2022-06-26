import re

import requests
from bs4 import BeautifulSoup
import wikipedia

# Use the web scraping wiki page as our starting point
response = requests.get(
    url="https://en.wikipedia.org/wiki/Fibonacci_number",
)

# Find an element by the ID tag using Beautiful soup
title = BeautifulSoup(response.content, 'html.parser').find(id="firstHeading")
#print("The title is : " + title.string)

# Specify the title of the Wikipedia page
wiki = wikipedia.page('Fibonacci_number')

# Extract the plain text content of the page
text = wiki.content
res = text.partition("== Definition ==")[0]

# print result
#print("String before the substring occurrence : " + res)

# Find an element by the name tag (img) using Beautiful soup
URL = "https://www.wikihow.com/Read-a-Candlestick-Chart" # Replace this with the website's URL
getURL = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
img = BeautifulSoup(getURL.text, 'html.parser').find_all('img')

# save in a variable only the img src
imageSources = []
for image in img:
    imageSources.append(image.get('src'))

# extract substring between two characters to get the first img link
pattern = "None\,(.*?)\, None,"
substring = re.search(pattern, str(imageSources)).group(1)
substring =substring[2:-1]
print(substring)
