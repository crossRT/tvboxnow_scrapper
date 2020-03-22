from django.apps import apps
from bs4 import BeautifulSoup
import requests
import re

session = None


def init():
    print('init scrapper session')
    global session
    session = requests.Session()


def login():
    print('scrapper logging in')
    config = apps.get_app_config('downloader')
    payload = {
        'username': config.username,
        'password': config.password
    }

    session.post('http://www.tvboxnow.com/logging.php?action=login&loginsubmit=yes', data=payload)
    print('login success')


def get_soup_by_url(link):
    response = session.get(link)
    body = response.content.decode(encoding='UTF-8')
    return BeautifulSoup(body, 'html.parser')


def get_drama_index():
    soup = get_soup_by_url('http://www.tvboxnow.com/forum-283-1.html')

    data = []
    for each_th in soup.find_all('th', {"class": "subject hot"}):
        span = each_th.find('span')
        a_tag = span.find('a')
        data.append({
            'name': span.text,
            'link': a_tag.get('href')
        })
    return data


# show all episodes of the drama
def get_drama_show(link):
    soup = get_soup_by_url(f'http://www.tvboxnow.com/{link}')

    data = []
    for item in soup.find_all('span', {'style': 'white-space: nowrap'}):
        a_tag = item.find('a')
        link = a_tag.get('href')
        if 'H265' in item.text:
            data.append({
                'name': item.text,
                'link': link,
            })
    return data


# download specific episode torrent
def get_drama_download(link):
    soup = get_soup_by_url(f'http://www.tvboxnow.com/{link}')

    all_p_tags = soup.find('p', string=re.compile('已扣除威望'))
    target_p_tag = all_p_tags.find_next_sibling()
    target_a_tag = target_p_tag.find('a')
    target_link = f"http://www.tvboxnow.com/{target_a_tag.get('href')}"

    response = session.get(target_link)
    file_name = re.findall('「(.+)」', all_p_tags.text)[0]
    config = apps.get_app_config('downloader')
    download_directory = config.download_directory
    full_path = download_directory + file_name
    open(full_path, 'wb').write(response.content)
