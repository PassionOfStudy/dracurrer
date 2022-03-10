# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
target_url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%B0%A9%EC%98%81+%EB%93%9C%EB%9D%BC%EB%A7%88&oquery=%08%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%93%9C%EB%9D%BC%EB%A7%88&tqi=hAD2wlprvhGssbW%2BB2NssssssjC-376765'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(target_url,headers=headers)
## utf-8로 바꾸어 주기
html = data.content.decode('utf-8', 'replace')
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(html, 'html.parser')
