from flask import Flask, render_template, url_for, request, redirect, jsonify, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import json
from PIL import Image
from io import BytesIO
import base64
import hashlib
from ops import StrDatabase, User
import xml.etree.ElementTree as elemTree
import os
# 부모 디렉토리
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 현재 디렉토리
current_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# secret_key를 관리하기 위해 xml 파일 사용
tree = elemTree.parse('keys.xml') # 사용 환경에 맞춰 절대 경로 적용 후 사용
app.secret_key = tree.find('string[@name="secret_key"]').text

# 로그인 관리
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 페이지의 엔드포인트 설정

# database 연결
db_pw = tree.find('string[@name="db_web_pw"]').text
db = StrDatabase(db_pw)

def render_template_with_banner(template_name: str, **context):
    """banner에 필요한 사용자 데이터를 함께 render_template()하기 위한 함수"""
    if current_user.is_authenticated:
        user_tuple = db.user_select(current_user.id)
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
    # 테스트용으로 작성한 코드
    # 아래 두줄은 배포할 때 삭제해야함
    image_name = "sample_image.png"
    path_type = "temp"
    if request.method == "POST":
        json_data = request.get_json()
        dict_data = json.loads(json.dumps(json_data))
        
        image_name = dict_data['name']
        if current_user.is_authenticated:
            path_type = current_user.id
        else:
            path_type = "temp"
            
        image_path = parent_path + f"/user/{path_type}/" + str(image_name)
        image_name = dict_data['img']
        image = Image.open(BytesIO(base64.b64encode(image_name)))
        image.save(image_path)
    
    return render_template_with_banner('/transfer/result.html', type=path_type, image = image_name)

@app.route('/<path_type>/<filename>')
def image_path(path_type, filename):
    return send_from_directory(parent_path + "/user/" + path_type, filename)

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
        return render_template_with_banner("/auth/register.html")

@app.route('/check_id', methods=['POST'])
def check_id():
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

@login_manager.user_loader
def load_user(user_id):
    try:
        result = db.user_select(user_id)
    except Exception as e:
        print(e)
        result = False
    if result:
        return User(user_id)
    return None

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data['user_id']
        user_pw = data['pw']
        user_pw = hash_password(user_pw)
        try:
            result = db.user_select(user_id)
        except Exception as e:
            print(e)
            result = False

        if result:
            if result[1] == user_pw:
                user = User(user_id)
                login_user(user)
                return jsonify({'exists': True, 'pw_match': True})
            else:
                return jsonify({'exists': True, 'pw_match': False})
        else:
            return jsonify({'exists': False, 'pw_match': False}) 
    else:
        return render_template_with_banner("/auth/login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def hash_password(password):
    """SHA-256으로 비밀번호를 해시합니다."""
    sha_signature = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return sha_signature

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

@app.route('/mypage')
def mypage():
    board_data = list(db.board_select_user(current_user.id))
    for i in range(len(board_data)):
        board_data[i] = list(board_data[i])
    
    savebox_data = list(db.savebox_select(current_user.id))
    for i in range(len(savebox_data)):
        savebox_data[i] = list(savebox_data[i])
    
    return render_template_with_banner("/member/mypage.html", board_data=board_data, savebox_data=savebox_data)

if __name__ == "__main__":
    app.run(debug=True)