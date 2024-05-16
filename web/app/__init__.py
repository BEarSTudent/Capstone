from flask import Flask, render_template, url_for, request, session, current_app, redirect, send_file
import json
from PIL import Image
from io import BytesIO
import base64
import os
import xml.etree.ElementTree as elemTree
app = Flask(__name__)

# secret_key를 관리하기 위해 xml 파일 사용
tree = elemTree.parse('web/keys.xml') # 사용 환경에 맞춰 절대 경로 적용 후 사용
app.secret_key = tree.find('string[@name="secret_key"]').text

@app.route('/')
def index():
    if 'id' in session:
        user_data = ["user_id", "사용자", "../static/images/sample_image.png"] # database 연결 후 데이터 불러오기
        return render_template("index.html", user_data=user_data)
    else:
        return render_template("index.html")

@app.route('/transfer')
def transfer_page():
    if 'id' in session:
        user_data = ["user_id", "사용자", "../static/images/sample_image.png"] # database 연결 후 데이터 불러오기
        return render_template("/transfer/transfer.html", user_data=user_data)
    else:
        return render_template("/transfer/transfer.html")

@app.route('/transfer/wait')
def wait():
    if 'id' in session:
        user_data = ["user_id", "사용자", "../static/images/sample_image.png"] # database 연결 후 데이터 불러오기
        return render_template("/transfer/wait.html", user_data=user_data)
    else:
        return render_template("/transfer/wait.html")

@app.route('/transfer/result', methods=["GET", "POST"])
def result():
    image_path = "images/sample_image.png"
    if request.method == "POST":
        json_data = request.get_json()
        dict_data = json.loads(json.dumps(json_data))
        
        image_name = dict_data['name']
        image_path = "images/transfer/" + str(image_name)

        image = dict_data['img']
        image = Image.open(BytesIO(base64.b64encode(image)))
        image.save(image_path)
    
    if 'id' in session:
        user_data = ["user_id", "사용자", "../static/images/sample_image.png"] # database 연결 후 데이터 불러오기
        return render_template("/transfer/result.html", user_data=user_data, image = image_path)
    else:
        return render_template('/transfer/result.html', image = image_path)

@app.route('/transfer/download/<path:filename>')
def download(filename):
    filename = "static/" + filename
    return send_file(filename,
                     as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
