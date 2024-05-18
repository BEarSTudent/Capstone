from flask import Flask, render_template, url_for, request, session, current_app, redirect, send_file, jsonify
import json
from PIL import Image
from io import BytesIO
import base64
import hashlib
from ops import StrDatabase, RegistrationForm
import xml.etree.ElementTree as elemTree

app = Flask(__name__)

# secret_key를 관리하기 위해 xml 파일 사용
tree = elemTree.parse('keys.xml') # 사용 환경에 맞춰 절대 경로 적용 후 사용
app.secret_key = tree.find('string[@name="secret_key"]').text

# database 연결
db_pw = tree.find('string[@name="db_web_pw"]').text
db = StrDatabase(db_pw)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data['user_id']
        try:
            result = db.user_select(user_id)
        except Exception as e:
            result = False
        if result:
            return jsonify({'exists': True, 'db_error': False})
        else:
            user_pw = data['pw']
            user_pw = hash_password(user_pw)
            user_name = data['user_name']
            try:
                db.user_insert(user_id, user_pw, user_name)
                print("redirect")
                return jsonify({'exists': False, 'db_error': False})
            
            except Exception as e:
                print("Unkwon Error: ", e)
                return jsonify({'exists': False, 'db_error': True})
                
    else:
        return render_template_with_banner("/member/register.html")

@app.route('/check_id', methods=['POST'])
def check_id():
    print("try 문")
    data = request.get_json()
    user_id = data['user_id']
    try:
        result = db.user_select(user_id)
    except Exception as e:
        print(e)
        result = False

    if result:
            return jsonify({'exists': True})
    else:
        return jsonify({'exists': False}) 
    

def hash_password(password):
    """SHA-256으로 비밀번호를 해시합니다."""
    sha_signature = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return sha_signature

if __name__ == "__main__":
    app.run(debug=True)
    db = StrDatabase()