from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
# 서버를 만져주는 지휘자
app = Flask(__name__)
# DB에 접근하기 위한 기능
client = MongoClient('localhost', 27017)
db = client.dbsparta
######################
# 1. HTML 화면 보여주기
######################
@app.route('/')
def home():
    return render_template('index.html')

######################
# 2. 데이터를 주고받는 기능, 영역
# 2-A. 새로고침 하면 DB에서 정보 가져와서 알아서 잘 보여줘
# 2-B. 좋아요 누르면, 그 영화배우 정보의 좋아요 수가 늘어남.
# 2-C. 삭제를 누르면, 그 영화배우 정보가 DB에서도 삭제됨
######################
@app.route('/api/list', methods=['GET'])
def show_stars():
    # 1. DB에 저장된 정보를 다 긁어와
    # 2. 좋아요 순서대로 정렬
    # 3. 묶어서 클라에 보내주자

    stars = list(
        db.mystar.find(
            {}, #모든 데이터를 가져와! 조건 없이!
            {'_id' : False}, # id 값을 없애주기 위해
        ).sort('like', -1) #like를 기준으로 내림차순
    )

    return jsonify({'result': 'success', 'stars_list': stars})

@app.route('/api/like', methods=['POST'])
def like_star():

    # 1. 유저가 뭘 보냈을까 확인하기
    name_received = request.form['name_give']
    # 2. 이름을 기준으로 DB에서 찾자
    star = db.mystar.find_one(
        {'name': name_received} #내가 받은 이름과 같은 data를 찾아!
    )

    #like수 업데이트
    # 3. 이름 = 유저가 보낸 이름 -> 데이터 ==> 업데이트.. like+1
    current_like = star['like']
    new_like = current_like + 1

    db.mystar.update_one(
        {'name': name_received},
        {'$set': {
            'like': new_like
        }}
    )

    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def delete_star():

    # 유저가 넘겨준 이름 정보를 받아
    name_received = request.form['name_give']

    #DB에서 데이터를 찾아
    db.mystar.delete_one(
        {'name':name_received}
    )

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)