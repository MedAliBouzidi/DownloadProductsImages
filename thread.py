
import os
import ssl
import sys
import json
import threading
import subprocess
import urllib.request

try:
    import unidecode as unidecode
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'unidecode'])
    import unidecode as unidecode


class Downloader:
    def __init__(self, urls, download_path):
        self.urls = urls
        self.download_path = download_path
        self.total_num = len(self.urls)
        t = threading.Thread(target=self.download())
        t.start()

    def download(self):
        status = ''
        for i, url in enumerate(self.urls, start=1):
            image_url = url['link']  # the image on the web
            save_name = f'{self.download_path}/{url["name"]}'  # local name to be saved
            if not os.path.exists(self.download_path):
                os.mkdir(self.download_path)
            if not os.path.exists(save_name):
                try:
                    urllib.request.urlretrieve(image_url, save_name)
                    status = 'done'
                except:
                    status = 'fail'
            print(f'{i}/{self.total_num} - {status}')
            i += 1


def normalize(s):
    return unidecode.unidecode(s)


def get_links():
    links_list = []
    with open('Products.json', encoding='utf-8') as f:
        data = json.load(f)
        for d in data:
            ext = d['image'].split('/')[-1].split('.')[-1]
            links_list.append({
                'name': f'{d["_id"]["$oid"]}.{ext}',
                'link': normalize(d['image'])
            })
    return links_list


if __name__ == '__main__':
    links = get_links()

    if not os.path.exists('images'):
        os.mkdir('images')

    ssl._create_default_https_context = ssl._create_unverified_context

    steps = 5_000
    for idx, index in enumerate(range(0, len(links), steps), start=1):
        Downloader(links[index:index + steps], f'images/{idx}')
