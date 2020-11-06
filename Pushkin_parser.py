from bs4 import BeautifulSoup
import requests

URL = 'https://istihi.ru/pushkin'
base_URl = 'https://istihi.ru'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


def get_links():
    column_elements = soup.find_all("ol", {"class": "dotted"})
    links = []
    for columns in column_elements:
        for a in columns.find_all('a'):
            links.append(a.get('href'))
    return links


def make_string(elem):
    final = ''
    for link in get_links():
        URL = base_URl + link
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        texts = soup.find("div", class_="poem-text")
        for string in texts.stripped_strings:
            final += (''.join(string.split('\n')))
    return final


with open("Pushkin.txt", "w+", encoding="utf-8") as text_file:
    text_file.write(make_string(get_links()))
