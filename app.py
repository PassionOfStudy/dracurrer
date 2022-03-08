from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # Main Page
    return render_template("index.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)