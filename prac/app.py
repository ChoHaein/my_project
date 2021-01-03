#-*- encoding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
# flask에서 Flask라는 지휘자를 꺼내줘

app = Flask(__name__) # 지휘자의 이름은 app 이야

########################
# 1. HTML을 보여주는 영역 #
########################

@app.route('/') # / 라는 주소(뒤에 아무것도 없음)로 들어오면 바로 밑에 있는 함수를 실행해줘
def hello_world():
    return render_template('index.html')

@app.route('/sample')
def show_sample():
    return 'This is sample page'

################################
# 2. 데이터를 가공해서 돌려주는영역 #
################################

@app.route('/test', methods=['GET'])
def test_get():
    # request의 구성요소(args)들 중에 title_give에 달린 정보를 가져와줘!
    received = request.args.get('title_get')
    print(received)
    return jsonify({
        'result' : 'success',
        'msg' : '이 요청은 GET 이었네요!'
    })

@app.route('/test', methods=["POST"])
def test_post():
    received = request.form['title_give']
    print(received)

    return jsonify({
        'result' : 'success',
        'msg' : '이 요청은 Post 입니다!'
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# http://localhost:5000/ 해당 주소로 들어가야 들어가짐