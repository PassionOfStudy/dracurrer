from crypt import methods
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# 아틀라스 몽고 DB접속
client = MongoClient('mongodb+srv://test:sparta@cluster0.jhcn4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbprojects

# 메인 
@app.route('/')
def main():
    return render_template('index.html')
    
# 게시글 등록페이지
@app.route('/register')
def registerPage():
    return render_template("register.html")

# 등록페이지에서 사용자가 등록한 드라마 URL을 수신하여 필요한 메타정보를 추출하여 저장하는 API
@app.route('/api/drama_lists', methods = ['POST'])
def saveDramaList():
    # 등록페이지에서 Form태그에서 POST로 보낸 값 가져오기
    if request.method == 'POST':
        result = request.form
        receive_url = result['drama_url']
        receive_title = result['board_title']

        # 사용자가 입력한 Dram URL을 받아 메타정보를 가져와 MongoDB에 저장한다
        target_url = receive_url
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(target_url,headers=headers)
        ## utf-8로 바꾸어 주기
        html = data.content.decode('utf-8', 'replace')
        # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
        soup = BeautifulSoup(html, 'html.parser')
        # 각 드라마 페이지의 메타정보를 추출
        # Q) 메타태그인 og를 이용한이유? og태그의 경우 표준규약이기 때문에 웹페이지를 만들 떄 공통됨
        drama_title = soup.select_one('meta[property="og:title"]')['content'];
        drama_image = soup.select_one('meta[property="og:image"]')['content'];
        drama_desc = soup.select_one('meta[property="og:description"]')['content'];

        doc = {
            'drama_title': drama_title,
            'drama_image': drama_image,
            'drama_desc': drama_desc
        }
        db.dracurrer.insert_one(doc);
        return jsonify({'msg': '등록이 완료되었습니다!'})

# MongoDB에 저장된 드라마관련 정보를 불러오는 API
@app.route('/api/drama_lists', methods = ['GET'])
def viewDramaList():
    drama_lists = list(db.dracurrer.find({}, {'_id':False}))
    return jsonify({'drama_lists': drama_lists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)