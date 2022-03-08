from crypt import methods
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.jhcn4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbprojects

@app.route('/', methods = ['POST', 'GET'])
def main():
    return render_template('index.html')
    
    
@app.route('/register')
def registerPage():
    return render_template("register.html")

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

@app.route('/api/drama_lists', methods = ['GET'])
def viewDramaList():
    drama_lists = list(db.dracurrer.find({}, {'_id':False}))
    return jsonify({'drama_lists': drama_lists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)