#-*- encoding: utf-8 -*-

from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

### Step 1. 서버, DB에 접근할 요소들을 미리 정의
# 1. 서버의 지휘자 정의
app = Flask(__name__)

# 2. DB에 들어가는 방법을 정의
client = MongoClient('localhost', 27017)
db = client.dbsparta

### Step 2. 본격적으로 서버 짜기

#1. HTML을 넘겨서 보여주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# 2. 필요한 기능을 정의하는 부분
# 2-A. 리뷰를 쓰고, DB에 저장시키는 개념 (POST)
@app.route('/review', methods=['POST'])
def write_review():
    # clien에서 보내준 데이터를 잘 가공해서 저장해주면 될듯?

    # 1. Client가 넘겨준 데이터 확인
    title_received = request.form['title_give']
    author_received = request.form['author_give']
    review_received = request.form['review_give']

    print(title_received)
    print(author_received)
    print(review_received)

    # 2.DB에 넣어줘!
    container = {
        'title' : title_received,
        'author' : author_received,
        'review' : review_received
    }

    # 3. DB에 넣어주기
    db.reviews.insert_one(container)

    return jsonify({
        'result' : 'success',
        'mgs' : '성공적으로 POST를 수행하였습니다!'
    })

# 2-B. DB에서 리뷰를 가져와서 보여주는 개념 (GET)
@app.route('/review', methods=['GET'])
def read_review():

    # DB에서 리뷰 정보 긁어다가 List로 넘겨주면 될듯?
    # DB에서 가져온 정보를 싹 다 reviews에 저장!
    reviews = list(db.reviews.find({}, {'_id':0}))

    return jsonify({
        'result' : 'success',
        'reviews' : reviews
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)