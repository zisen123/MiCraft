import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import zipfile


# Define some directory DIR
SCRIPTS_DIR=os.path.abspath('.')
ROOT_DIR=os.path.split(SCRIPTS_DIR)[0]
DOWNLOAD_DIR=os.path.join(ROOT_DIR,'downloads')
SERVER_DIR=os.path.join(ROOT_DIR,'server')
URL_MOJANG='https://www.minecraft.net/en-us/download/server/bedrock'


# Find the download url using requests with UA and BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
}
response = requests.get(URL_MOJANG, headers=headers, stream=True)

response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.content, 'lxml')

hyperlink = bs.find(attrs={'aria-label': "Download Ubuntu Server software for Ubuntu"})

URL_DOWNLOAD= hyperlink.attrs['href']


# Create directory downloads if not exists
if not os.path.exists(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

# Chech if the server is the latest
# Download the latest server file
SERVER_NAME=URL_DOWNLOAD.split('/')[-1]
SERVER_FILE=os.path.join(DOWNLOAD_DIR,SERVER_NAME)

"""
r = requests.get(URL_DOWNLOAD)
with open(SERVER_FILE, 'wb') as f:
    f.write(r.content)
"""

def download(url: str, fname: str):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

download(URL_DOWNLOAD,SERVER_FILE)

# Create directory downloads if not exists
if not os.path.exists(SERVER_DIR):
    os.mkdir(SERVER_DIR)
# Express the file to server directory
archive = zipfile.ZipFile(SERVER_FILE)

for file in archive.namelist():
    archive.extract(file, SERVER_DIR)