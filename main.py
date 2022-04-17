import re
import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response.text

def get_titles(html):
    soup = BeautifulSoup(html, 'lxml')
    pattern = r'^https://kissanime.tube/movie/'
    animes = soup.find_all('a', href=re.compile(pattern))
    return animes

def get_title_data(title):
    url = "https://kissanime.tube/home/"
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    try:
        a_title = soup.find('h3', class_="jtitle").text.strip()
    except:
        title = ""
        print(url)

def main():
    all_animes = []
    url = "https://kissanime.tube/home/"

    while True:
        animes = get_titles(get_html(url))
        if animes:
            all_animes.extend(animes)
            url = "https://kissanime.tube/home/"
        else:
            break

    for anime in animes:
        title = anime.get('data-jtitle')