from crypt import methods
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import jwt  # pyjwt 모듈도 함께 설치해줘야함.
import datetime
import hashlib
# h5py ?? 아직 잘 모르겠음
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

################################################################################################################################################
# 아틀라스 몽고 DB접속
## 로그인을 위한 MongoDB 접속 ##
## cilient = 회원가입 & 로그인 DB , client2 = 드라마 크롤링정보 및 게시판 타이틀 DB, client3 = 게시판 리뷰 작성 DB ##
client = MongoClient('mongodb+srv://test:sparta@cluster0.rmyvw.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
client2 = MongoClient('mongodb+srv://test:sparta@cluster0.jhcn4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db2 = client2.dbprojects
client3 = MongoClient('mongodb+srv://wlsgurdl54:dngkgk5415!@cluster0.rqgeg.mongodb.net/Cluster0?retryWrites=true&w=majority')
db3 = client.dbsparta

## 리스팅 기능 구현 및 사용자 게시판 등록 페이지 구현 ##
################################################################################################################################################  
@app.route('/')
def main():
    drama_lists = list(db2.dracurrer.find({}, {'_id':False}))
    return render_template('index.html', drama_lists=drama_lists)

@app.route('/register')
def register():
    return render_template('register.html')

# 사용자 입력 url수신하여 drama 정보를 크롤링하여 저장하는 API
@app.route('/dramalists', methods=['POST'])
def saveList():
    # 등록페이지에서 Form태그에서 POST로 보낸 값 가져오기
    if request.method == 'POST':
        result = request.form
        receive_url = result['url_give']
        receive_title = result['title_give']

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
        db2.dracurrer.insert_one(doc);
        return jsonify({'msg': '등록이 완료되었습니다!'})

@app.route('/dramalists', methods=['GET'])
def showList():

    return jsonify({'msg': '보여주기 완료!'})

############################################################################################################
## 로그인 기능 구현 ##
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash  # 비밀번호
        # "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        # "profile_pic": "",  # 프로필 사진 파일 이름
        # "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        # "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})
################################################################################################################################################
## 게시판 리뷰 기능 구현 ##
@app.route('/review')
def home():
    return render_template('review.html')

@app.route('/api/review', methods=['GET'])
def show_review():
    reviews = list(db.review.find({}, {'_id': False}))
    return jsonify({'all_review': reviews})

@app.route('/api/review', methods=['POST'])
def save_review():
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']
    star_receive = request.form['star_give']

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'


    save_to = f'static/{filename}.{extension}'
    file.save(save_to)


    doc = {
        'title':title_receive,
        'contents':contents_receive,
        'star':star_receive,
        'file':f'{filename}.{extension}',
        'time':today.strftime('%Y.%m.%d')
    }

    db.review.insert_one(doc)


    return jsonify({'msg': '리뷰가 등록되었습니다!'})
################################################################################################################################################
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
