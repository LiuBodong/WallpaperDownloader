import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from os import path
import os
import urllib3

urllib3.disable_warnings()

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))


base_url = 'https://www.xiezhen.world/'
save_path = '/home/zodiac/Data/xiezhenmen'

cookies = session.get(base_url,
                      verify=False, timeout=(3, 3)).cookies

def get_articles(url):
    articles = []
    response = session.get(url, cookies=cookies,
                           verify=False, timeout=(3, 3))
    if response.status_code == 200:
        content = str(response.content, 'utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        a = soup.select('article > h2 > a')
        for article in a:
            name = article.string
            href = article['href']
            articles.append({'name': name, 'href': href})
    return articles


def get_pics(url):
    pics = []
    response = session.get(url, cookies=cookies,
                           verify=False, timeout=(3, 3))
    if response.status_code == 200:
        content = str(response.content, 'utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        imgs = soup.find('article', class_='article-content').find_all('img')
        for img in imgs:
            href = img['src']
            name = href.split('/')[-1]
            pics.append({'name': name, 'href': href})
    return pics


page = 1
url = base_url + 'page/' + str(page) + '/'
articles = get_articles(url)
while articles:
    print('开始下载第[' + str(page) + '页]')
    for article in articles:
        name = article['name']
        print('开始下载[' + name + ']')
        save_dir = path.join(save_path, name)
        if not path.exists(save_dir):
            os.makedirs(save_dir)
        pics = get_pics(article['href'])
        for pic in pics:
            pic_name = pic['name']
            pic_href = pic['href']
            save_file = path.join(save_dir, pic_name)
            if path.exists(save_file):
                print(save_file + '已存在')
            else:
                response = session.get(
                    pic_href, cookies=cookies, verify=False, timeout=(3, 3))
                if response.status_code == 200:
                    with open(save_file, 'wb+') as f:
                        f.write(response.content)
                        print('下载到' + save_file)
    page += 1
    url = base_url + 'page/' + str(page) + '/'
    articles = get_articles(url)
