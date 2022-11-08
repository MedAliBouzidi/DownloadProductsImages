import json
import os
import ssl
import urllib.request

links = []
with open('Products.json', encoding='utf-8') as f:
    data = json.load(f)
    for d in data:
        ext = d['image'].split('/')[-1].split('.')[-1]
        links.append({
            'name': f'{d["_id"]["$oid"]}.{ext}',
            'link': d['image']
        })

if not os.path.exists('images'):
    os.mkdir('images')

total_num = len(links)

ssl._create_default_https_context = ssl._create_unverified_context

for idx, image in enumerate(links, start=1):
    image_url = image['link']  # the image on the web
    save_name = f'images/{image["name"]}'  # local name to be saved
    urllib.request.urlretrieve(image_url, save_name)
    print(f'{idx}/{total_num}')
