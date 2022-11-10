import os
import ssl
import json
import urllib.request

index = 4

with open('json/j4.json', encoding='utf-8') as f:
    links = json.load(f)

if not os.path.exists('images'):
    os.mkdir('images')

ssl._create_default_https_context = ssl._create_unverified_context

total_num = len(links)

for idx, image in enumerate(links, start=1):
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
