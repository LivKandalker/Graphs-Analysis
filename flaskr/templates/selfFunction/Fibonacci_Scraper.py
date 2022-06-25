import requests
from bs4 import BeautifulSoup
import wikipedia

# Use the web scraping wiki page as our starting point
response = requests.get(
    url="https://en.wikipedia.org/wiki/Fibonacci_number",
)

# Find an element by the ID tag using Beautiful soup
title = BeautifulSoup(response.content, 'html.parser').find(id="firstHeading")
print("The title is : " + title.string)

# Specify the title of the Wikipedia page
wiki = wikipedia.page('Fibonacci_number')

# Extract the plain text content of the page
text = wiki.content
res = text.partition("== Definition ==")[0]

# print result
print("String before the substring occurrence : " + res)
