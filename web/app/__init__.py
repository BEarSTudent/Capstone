from flask import Flask, render_template, url_for, request, session, current_app, redirect, send_file, jsonify
import json
from PIL import Image
from io import BytesIO
import base64
import os
import xml.etree.ElementTree as elemTree
from ops import strdb
app = Flask(__name__)

# secret_key를 관리하기 위해 xml 파일 사용
tree = elemTree.parse('web/keys.xml') # 사용 환경에 맞춰 절대 경로 적용 후 사용
app.secret_key = tree.find('string[@name="secret_key"]').text

# database 연결
db_pw = tree.find('string[@name="db_web_pw"]').text
db = strdb.StrDatabase(db_pw)

def render_template_with_banner(template_name: str, **context):
    """banner에 필요한 사용자 데이터를 함께 render_template()하기 위한 함수"""
    if 'id' in session:
        user_tuple = db.user_select(session['id'])
        user_data = (user_tuple[0], user_tuple[2], user_tuple[3])
        return render_template(template_name, user_data=user_data, **context)
    else:
        return render_template(template_name, **context)

@app.route('/')
def index():
    return render_template_with_banner("index.html")

@app.route('/transfer')
def transfer_page():
    return render_template_with_banner("/transfer/transfer.html")

@app.route('/transfer/wait')
def wait():
    return render_template_with_banner("/transfer/wait.html")

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
    
    return render_template_with_banner('/transfer/result.html', image = image_path)

@app.route('/transfer/download/<path:filename>')
def download(filename):
    filename = "static/" + filename
    return send_file(filename,
                     as_attachment=True)

@app.route('/community', methods=["GET"])
def community():
    search_text = request.args.get('search_text')
    sort_by = request.args.get('select_order')
    
    if search_text == None:
        search_text = ""
    
    boards = list(db.board_select(search_text, sort_by))
    for i in range(len(boards)):
        boards[i] = list(boards[i])
    
    return render_template_with_banner("/community/community.html", search_text=search_text, sort_by=sort_by, board_data=boards)

if __name__ == "__main__":
    app.run(debug=True)
