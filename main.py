import json
import os
import ssl
import urllib.request

import unidecode as unidecode


def normalize(s):
    return unidecode.unidecode(s).lower()


links = []
with open('Products.json', encoding='utf-8') as f:
    data = json.load(f)
    for d in data:
        ext = d['image'].split('/')[-1].split('.')[-1]
        links.append({
            'name': f'{d["_id"]["$oid"]}.{ext}',
            'link': normalize(d['image'])
        })

if not os.path.exists('images'):
    os.mkdir('images')

total_num = len(links)

ssl._create_default_https_context = ssl._create_unverified_context

chunks = [links[index:index + 2000] for index in range(0, len(links), 2000)]

idx = 0
for chunk in chunks:
    for image in chunk:
        image_url = image['link']  # the image on the web
        save_name = f'images/{image["name"]}'  # local name to be saved
        if not os.path.exists(save_name):
            urllib.request.urlretrieve(image_url, save_name)
        idx += 1
        print(f'{idx}/{total_num}')
