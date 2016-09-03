import os

import requests
import subprocess
from lxml import html

from .config import NRT_USER, NRT_PASS, DOWNLOAD_DIR

DOWNLOAD_URL = 'http://www.newreleasetoday.com/freemusic1.php'
LOGIN_URL = 'http://www.newreleasetoday.com/loginrequired1.php'
MP3_URL_XPATH = '//div[@class="overWriteFont"]/table[1]//table[1]//table[1]//table[1]/tr[2]/td/a/@href'


def find_mp3_urls():
    payload = {'name': NRT_USER, 'password': NRT_PASS}
    with requests.Session() as s:
        s.post(LOGIN_URL, data=payload)
        r = s.get(DOWNLOAD_URL)
        tree = html.fromstring(r.text)
        return tree.xpath(MP3_URL_XPATH)


def download_mp3(mp3_url):
    final_url = requests.head(mp3_url, allow_redirects=True).url
    local_filename = os.path.join(DOWNLOAD_DIR, final_url.split('/')[-1])
    if not os.path.isfile(local_filename):
        r = requests.get(final_url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        show_msg('MP3 downloaded', 'File {} downloaded from {}'.format(os.path.basename(local_filename), final_url))


def show_msg(main_msg, sub_msg):
    subprocess.Popen(['notify-send', main_msg, sub_msg])


def main():
    show_msg('Start NRT download', '')
    urls = find_mp3_urls()
    for url in urls:
        download_mp3(url)
