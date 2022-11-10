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

if not os.path.exists('json'):
    os.mkdir('json')

i = 1
for index in range(0, len(links), 5000):
    with open(f'json/j{i}.json', 'w', encoding='utf-8') as f:
        json.dump(links[index:index + 5000], f)
        i += 1

idx = 0
for index, chunk in enumerate(chunks, start=1):
    for image in chunk:
        image_url = image['link']  # the image on the web
        save_name = f'images/{index}/{image["name"]}'  # local name to be saved
        if not os.path.exists(f'images/{index}'):
            os.mkdir(f'images/{index}')
        if not os.path.exists(save_name):
            try:
                urllib.request.urlretrieve(image_url, save_name)
            except:
                continue
        idx += 1
        print(f'{idx}/{total_num}')
