import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
}

response = requests.get('https://www.minecraft.net/en-us/download/server/bedrock', headers=headers)

response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.content, 'lxml')

hyperlink = bs.find(attrs={'aria-label': "Download Ubuntu Server software for Ubuntu"})

url = hyperlink.attrs['href']

print(url)