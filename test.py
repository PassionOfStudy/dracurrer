# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
target_url = 'https://program.kbs.co.kr/2tv/drama/crazylove2022/pc/index.html'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(target_url,headers=headers)
## utf-8로 바꾸어 주기
html = data.content.decode('utf-8', 'replace')
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(html, 'html.parser')

title = soup.select_one('meta[property="og:title"]')['content'];
image = soup.select_one('meta[property="og:image"]')['content'];
desc = soup.select_one('meta[property="og:description"]')['content'];

doc = {
    'drama_title': title,
    'drama_image': image,
    'drama_desc': desc
}

